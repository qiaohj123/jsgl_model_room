import cx_Oracle
from jsgl_model_room.CommonLib.PublickLib import *
import json
import pymysql


class OracleAction:
    def __init__(self):
        self.username_225 = GetConfig('oracle_data_225', 'data_name').getpath()
        self.password_225 = GetConfig('oracle_data_225', 'data_password').getpath()
        self.host_225 = GetConfig('oracle_data_225', 'host_name').getpath()

        self.username_253 = GetConfig('oracle_data_253', 'data_name').getpath()
        self.password_253 = GetConfig('oracle_data_253', 'data_password').getpath()
        self.host_253 = GetConfig('oracle_data_253', 'host_name').getpath()

        self.username_7 = GetConfig('mysql_data_7', 'user_name').getpath()
        self.password_7 = GetConfig('mysql_data_7', 'password').getpath()
        self.host_7 = GetConfig('mysql_data_7', 'host_name').getpath()
        self.db_name = GetConfig('mysql_data_7', 'data_name').getpath()

    def connect_cursor(self, data):
        if data == '225':
            connect = cx_Oracle.connect(self.username_225, self.password_225, self.host_225)
            return connect
        elif data == '253':
            connect = cx_Oracle.connect(self.username_253, self.password_253, self.host_253)
            return connect
        elif data == '7':
            connect = pymysql.connect(host=self.host_7, user=self.username_7, passwd=self.password_7, db=self.db_name, port=3306, charset='utf8')
            return connect

    def sql_action(self, data, pro='', types='', sql='', es_id='', style='', query='query'):
        con = self.connect_cursor(data)
        cur = con.cursor()
        # params = {'table': table, 'field': field}
        # cur.execute('select :table from :field', params)
        if pro != '':   # oracle存储过程
            if types == 'oracle':
                cur.callproc(pro, [es_id])   # oracle存储过程
            elif types == 'mysql':
                cur.callproc(pro, (es_id,))  # mysql存储过程
            con.commit()
            cur.close()
            con.close()
        else:
            cur.execute(sql)
            if style != '':   # 处理超长型字段值
                pram = []
                for row in cur:
                    txt = row[0].read()
                    pram.append(txt)
                cur.close()
                con.close()
                return pram
            elif query == 'query':
                rows = cur.fetchone()
                cur.close()
                con.close()
                return rows
            elif query == 'update' or 'insert':
                con.commit()
                cur.close()
                con.close()

    # 获取指令值--225数据库中获取指令及es_id列表
    def order_exe(self):
        # order = self.sql_action('225', 'select * from ACT_RU_TASK')
        order = self.sql_action('225', sql='select * from es.esm_sample_house a where a.state= 1')
        order_list = []
        if order is None:
            order_list = ['0', '0', '0']
        else:
            order_list.append(order[0])  # 业务id
            order_list.append('1')  # 指令赋值为1
            order_list.append(order[1])  # ('1', '9582F0F1-9687-41FD-A030-E12F43F0E04E', '1',  None, None, None, None)
        return order_list

    # 设定（重置）指令值
    def set_order_value(self):
        self.sql_action('225', sql="update es.esm_sample_house a set a.state= '2' where a.state='1'", query='update')

    # 调用建管平台存储过程
    def call_procedure(self, es_id):
        # es_id = self.order_exe()[1]
        self.sql_action('253', pro="proc_get_sample_house_json", types='oracle', es_id=es_id)

    # 调用质检平台存储过程
    def call_procedure_zj(self, es_id):
        # es_id = self.order_exe()[1]
        self.sql_action('7', pro="form_data_to_json", types='mysql', es_id=es_id)

    # 获取填报数据--253数据库中获取 建管相关数据
    def data_to_dict(self, es_id, item_list):
        sql = "select DATA from anc_demo_data where ES_ID='{}'".format(es_id)
        result_data = self.sql_action('253', style='1', sql=sql)
        result_rel = json.loads(result_data[0])
        if item_list == '收方单':
            sfd = result_rel['sfd']
            return sfd
        elif item_list == '项目标段':
            bid_section = {}
            bid_section["标段ID"] = result_rel['sectionId']
            bid_section["标段"] = result_rel['sectionNum']
            bid_section["分项结构"] = result_rel['strName']
            return bid_section

    # 更新现场收方单审核状态为 审核通过
    def update_sfd_state(self, section_name):
        sql = "update mms_confirm_qua_main set report_state = 2 where no = (select no from mms_confirm_qua_main where title='{}')".format(section_name)
        self.sql_action('253', query='update', sql=sql)

    # 更新中期支付证书审核状态为 审核通过
    def update_zqzs_state(self, section_id):
        sql ="update mms_middle_certificate_main set report_state = '2' where section_id = '{}' and create_time = (select max(create_time) from mms_middle_certificate_main where section_id = '{}')".format(section_id, section_id)
        self.sql_action('253', query='update', sql=sql)

    # 获取质检-开工报告表单数据--11.7数据中
    def data_to_dict_zj(self, es_id, request=''):
        sql = "select json from sample_test where project_node_id='{}'".format(es_id)
        result_data = self.sql_action('7', sql=sql)
        result_rel = json.loads(result_data[0])
        report_list = {}  # 主表与子表键值对
        main_list = []
        if request == 'sub_list':
            for i in result_rel:
                sub_list = []
                if i['instances'] != []:
                    for j in i['instances']:
                        sub_list.append(j['name'])
                    # print(sub_list)
                    report_list[i['name']] = sub_list

            print(report_list.keys())
            return report_list
        elif request == 'keys':
            for m in result_rel:
                main_list.append(m['name'])
            print(main_list)
            return main_list


    # 视频文件数据插入253库中
    def video_file_into_data(self, video_file_name, house_id):
        visit_dir = 'http://jg.scgsdsj.com/ftp/jg/product/HOUSE/{}.mp4'.format(video_file_name)
        sql = "insert into auth_attach_files(ID,FILE_NAME,UPLOAD_DATE,FILE_TYPE,URL,AFFILATION_ID,STATE,ROOT,PATH,ACT_NAME,SERVER_URL) values(sys_guid(),'{}.mp4',sysdate,'video','product/HOUSE','{}','0','/opt/File_Upload/','house','{}.mp4','{}')".format(video_file_name, house_id, video_file_name, visit_dir)
        self.sql_action('225', query='insert', sql=sql)



#
# a = OracleAction()
# a.call_procedure_zj()

# a.video_file_into_data('testfilename', '2223423')
# a.video_file_into_data('1','2')
# #
# #     def return_receipt(self):
# #         a = {"projectId": "6856ed849630462489c63c6ac5407efa",
# #              "proName": "乐山至西昌高速公路马边至昭觉段工程项目",
# #              "sectionId": "bbfe97d640534ad1add284085c1b9ca5",
# #              "sectionNum": "K1",
# #              "strName": "K73+950-K74+025段超前小导管",
# #              "sfd": [{"upName": "谷堆互通式立交K0+212.486A匝道中桥",
# #                       "item_num": "420-2-e-2",
# #                       "quantity": "1629",
# #                       "item_name": "换填片（碎）石",
# #                       "formula": "换填片（碎）石：(1+8.8+1)*1*150.81=1629m3"},
# #                      {"upName": "谷堆互通式立交K0+212.486A匝道中桥",
# #                       "item_num": "420-2-f-1",
# #                       "quantity": "2172",
# #                       "item_name": "结构挖土方",
# #                       "formula": "涵洞挖土方：每延米14.4m3*150.81=2172m3"},
# #                      {"upName": "谷堆互通式立交K0+212.486A匝道中桥",
# #                       "item_num": "420-2-f-2",
# #                       "quantity": "3257",
# #                       "item_name": "结构挖石方",
# #                       "formula": "涵洞挖石方：每延米21.6m3*150.81=3257m3"}]}
# #         return a['sfd']
# #
# a = OracleAction()
# # a.data_to_dict_zj()
# txt = a.data_to_dict(item_list='项目标段')
# print(type(txt))
# print(txt)
# print(txt['标段'])
# print(type(txt['标段']))