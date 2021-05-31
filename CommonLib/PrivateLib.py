from jsgl_model_room.CommonLib.PublickLib import *
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import os

'''
login() 系统登录
windows_handle() 窗口切换
get_report_element()  表单元素获取-例：第5行，第8列的参数为（4,8）--建管主页面及质检评定页面使用
receipt_cell() 现场收方单--表格数据填写--(0,5)表示第1行第6列
main_frame() 登录后从主框架切换到“我的菜单”框架
men_choice() 进入更多页面-进行模块选择
section_id() 工程结构中期支付证书标段选择
upload_certificate_file()  中期支付证书上报
back_certificate_file()  中期支付证书驳回
upload_times()  工程结构中期支付证书操作---多次上报
receipt_choice() 现场收方单--选择工程结构
add_receipt() 现场收方单--新增-报表数据填写
upload_receipt() 现场收方单--上报审核
measure_choice() 中间计量-标段选择
measure_increase() 新增中间计量（已收方）
work_check() 工序检查分部分项工程搜索
details_read()  工序检查详情查看
back_firstpage() 从业务页面返回到首页页面
quality_page() 质检评定页面切换
section_search() 质检评定页面分项工程搜索
add_report() 质检评定页面--添加表单
write_report()  质检评定页面--添加子表、编辑保存
auditing_examine() 质检评定页面--批量提交审核

'''


class PrivateModule:
    def __init__(self, dr):
        self.dr = dr
        self.ele = VisibleElement(self.dr)
        self.log = Log()
        self.dr.maximize_window()

# 公共功能== == == == 优 == == == == 雅 == ==== == = 的 == ==== == == 分 == == ==== == = 隔 == == == == == == 线 == == == ==

    # 窗口切换，切换到最新窗口
    def windows_handle(self, old='null'):
        self.log.info('>>> 浏览器窗口切换')
        windows = self.dr.window_handles
        if old == 'null':
            # 切换到最新窗口
            try:
                self.dr.switch_to.window(windows[-1])
                self.log.info('>>> 窗口切换完成')
            except Exception as e:
                self.log.warning('>>> 浏览器窗口切换失败')
                raise e
        else:
            # 切换到第一个窗口
            try:
                self.dr.switch_to.window(windows[int(old)])
                self.log.info('>>> 窗口切换完成')
            except Exception as e:
                self.log.warning('>>> 浏览器窗口切换失败')
                raise e

    # 表单元素获取-例：第5行，第8列的参数为（4,8）--建管主页面及质检评定页面使用
    def get_report_element(self, row_s, clu_s, alls='null'):
        try:
            table = self.ele.find_ele('class', 'ant-table-tbody')  # 质检表格
            # table = self.ele.find_ele('id', 'tableId')  # 建管表格
            # 获取列表表格的行数
            table_rows = table.find_elements_by_tag_name('tr')
            # 获取列表单元格数据
            data = table_rows[row_s].find_elements_by_tag_name('td')[clu_s]
            if alls == 'null':
                return data
            else:
                return table_rows
        except Exception as e:
            Log().warning("获取单元格数据失败%s" % (e))
            raise e

    # 现场收方单--表格数据填写--(0,5)表示第1行第6列
    def receipt_cell(self, row_s, clu_s):
        try:
            table = self.ele.find_ele('class', 'el-table__body')
            # 获取列表表格的行数
            table_rows = table.find_elements_by_tag_name('tr')
            # 获取列表单元格数据
            data = table_rows[row_s].find_elements_by_tag_name('td')[clu_s]
            # data.find_element_by_class_name('el-input__inner').send_keys('111')
            return data
        except Exception as e:
            Log().warning("获取单元格数据失败%s" % (e))
            raise e

    def apply_style(self, element, action=''):
        new_style = 'background: green; border: 2px solid red;'
        old_style = element.get_attribute('style')
        self.dr.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, new_style)
        time.sleep(0.5)
        if action == '':
            element.click()
        else:
            ActionChains(self.dr).move_to_element(element).click().perform()
        self.dr.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, old_style)
        time.sleep(0.5)


# 建管模块功能== == == == 优 == == == == 雅 == ==== == = 的 == ==== == == 分 == == ==== == = 隔 == == == == == == 线 == == == ==

    # 系统登陆
    def login(self):
        self.log.info('>>> 登录系统')
        # 请求登录地址
        self.dr.get(GetConfig('logindata', 'url_module').getpath())
        # 输入登录用户名
        self.ele.find_ele('name', 'username').send_keys(GetConfig('logindata', 'username').getpath())
        # 输入登录密码
        self.ele.find_ele('name', 'password').send_keys(GetConfig('logindata', 'password').getpath())
        # 输入验证码
        self.ele.find_ele('id', 'retrieve').send_keys(GetConfig('logindata', 'logincode').getpath())
        # 点击登录
        self.ele.find_ele('id', 'loginBtn').click()
        self.log.info('>>> 系统登录成功')
        # time.sleep(3)
        # 判断页面是否存在密码输入框及任务提示框
        try:
            self.ele.find_ele('class', 'layui-layer-btn1', timeout=3).click()  # 待办任务提醒
            self.ele.find_ele('class', 'layui-layer-setwin', timeout=0.5).click()  # 密码更新提醒
        except Exception as E:
            pass

    # 登录后从主框架切换到“我的菜单”框架
    def main_frame(self):
        f1 = self.ele.find_ele('name', 'home')
        self.dr.switch_to.frame(f1)

    # 进入更多页面-进行模块选择
    def men_choice(self, first_module, out='null', second_name='null'):
        # 获取对应模块资源id
        first_id = ''
        second_id = ''
        # 一级单模块：名称与id资源字典集
        first_dic = {'工序检查': 'menu_ABA7548E128CC5ADE053201010AC17AD',
                     '进度计划': 'menu_8AF074763F117618E050007F0100DA4A',
                     '质检评定': 'menu_AE17C2FAB30DDA2AE053201010AC1E9C',
                     '工程结构计量': 'menu_9942B8AF5B1922ECE053E00910AC688D',
                     '电子档案': 'menu_B7A4BDF935529D6DE053201010AC2E45',
                     '基础资料': 'menu_5B2E2B7A3CEE49EEA770DDC88892F56B'}
        # 二级菜单模块：名称与id资源字典集
        second_dic = {'年度计划': 'menu1_E413E16D2411432BA1BCFFD6E4BF953B',
                      '中期支付证书': 'menu1_9942B8AF5B1B22ECE053E00910AC688D',
                      '现场收方单': 'menu1_A59304E6AEA70611E053E10910ACF0C3',
                      '中间计量': 'menu1_9942B8AF5B1A22ECE053E00910AC688D',
                      'WBS结构': 'menu1_983761A667A92E12E053E00910ACB0BB'}
        # 获取一级菜单id
        for first_key in first_dic:
            if first_key == first_module:
                first_id = first_dic[first_key]
            else:
                pass
        # 点击更多按钮
        # time.sleep(1)
        g1 = self.ele.find_ele('xpath', '//div[@class="center-menu-div"]/div[2]/div[5]/div[1]')  # 易报错体质
        self.apply_style(g1)
        # 在更多页面查询一级菜单
        time.sleep(1)
        self.ele.find_ele('xpath', '//input[@placeholder="请输入内容..."]').send_keys(first_module)

        # 内部菜单——跳转情况(非外接系统)
        if out == 'null':
            # 跳转-——不存在二级菜单情况
            if second_name == 'null':
                # self.ele.find_ele('id', '%s' % first_id).click()
                g2 = self.ele.find_ele('id', '%s' % first_id)
                self.apply_style(g2)
                # 从菜单层级框架切换到业务页面框架
                self.dr.switch_to.parent_frame()
                frame_id1 = first_id[5:]
                f2 = self.ele.find_ele('xpath', '//div[@id= "' + frame_id1 + '"]/iframe')
                self.dr.switch_to.frame(f2)

            # 跳转——存在二级菜单情况
            else:
                for second_key in second_dic:
                    if second_key == second_name:
                        second_id = second_dic[second_key]
                    else:
                        pass
                main_ele = self.ele.find_ele('id', '%s' % first_id)
                # ActionChains(self.dr).move_to_element(main_ele).perform()
                self.apply_style(main_ele, '1')
                # 当模块添加到首页菜单时，这个模块所有的元素存在两个相同属性值；当没有添加时，则只有唯一一个属性值。需要做判断
                # 首页我的菜单为第二个元素，更多页面的为第一个元素
                elements = self.dr.find_elements_by_id('%s' % second_id)
                time.sleep(1.5)
                # elements[0].click()
                self.apply_style(elements[0])
                # 从菜单层级框架切换到业务页面框架
                self.dr.switch_to.parent_frame()
                frame_id = second_id[6:]
                f2 = self.ele.find_ele('xpath', '//div[@id= "' + frame_id + '"]/iframe')
                self.dr.switch_to.frame(f2)
        else:
            # self.ele.find_ele('id', '%s' % first_id).click()
            g3 = self.ele.find_ele('id', '%s' % first_id)
            self.apply_style(g3)
            # 切换到最新的窗口
            self.log.info('>>> 切换到外部系统最新窗口')
            self.windows_handle()

    # 工程结构中期支付证书标段选择
    def section_id(self, section_id):
        self.ele.find_ele('id', 'sectionId').click()
        self.ele.find_ele('xpath', '//option[text()="' + section_id + '"]').click()
        time.sleep(1)

    # 中期支付证书新增
    def add_certificate_file(self):
        self.ele.find_ele('class', 'icon-xinzeng').click()
        time.sleep(1)
        f1 = self.ele.find_ele('xpath', '//div[@class="layui-layer-content"]/iframe')
        self.dr.switch_to.frame(f1)
        self.ele.find_ele('xpath', '//input[@value="提 交"]').click()
        self.dr.switch_to.parent_frame()
        time.sleep(4)
        self.ele.find_ele('xpath', '//td[text()="未审核"]/following-sibling::td//a').click()
        time.sleep(3)
        self.windows_handle()
        self.upload_certificate_file()
        time.sleep(10)

    # 审核上报
    def upload_certificate_file(self):
        self.ele.find_ele('xpath', '//span[text()="上报"]', 10).click()
        time.sleep(1)
        self.ele.find_ele('xpath', '//div[@class="el-message-box__btns"]/button[2]').click()
        # 选择上报人员
        try:
            self.ele.find_ele('class', 'el-dialog__body', 1)
            time.sleep(1)
            self.ele.find_ele('xpath', '//span[text()="乐西管理员"]').click()
            time.sleep(1)
            self.ele.find_ele('class', 'el-icon-arrow-right').click()
        except Exception as e:
            pass
        self.log.info('>>> 提交上报')
        time.sleep(1)
        self.ele.find_ele('xpath', '//span[text()="提交"]').click()
        time.sleep(1)
        # t1 = time.time()
        # return t1
        # self.ele.find_ele('xpath', '//span[text()="驳回"]', 1200).click()
        # t2 = time.time()
        # self.log.info(
        #     ">>> K2上报耗费时长为（s）：{0}".format(int(round((t2 - t1)))))

    # 中期支付证书驳回
    def back_certificate_file(self):
        self.ele.find_ele('xpath', '//span[text()="驳回"]', 10).click()
        time.sleep(2)
        self.ele.find_ele('xpath', '//div[@class="el-textarea"]/textarea').send_keys('测试驳回')
        self.ele.find_ele('xpath', '//span[text()="驳 回"]').click()
        self.ele.find_ele('xpath', '//div[@class="el-message-box__btns"]/button[2]').click()

    # 工程结构中期支付证书操作---多次上报
    def upload_times(self):
        self.windows_handle()
        for i in range(1, 10000):
            try:
                t1 = self.upload_certificate_file()
                self.ele.find_ele('xpath', '//span[text()="驳回"]', 300)
                t2 = time.time()
                self.log.info(
                    ">>> 上报耗费时长为（s）：{0}".format(int(round((t2 - t1)))))

            except Exception as e:
                self.back_certificate_file()
                self.ele.find_ele('xpath', '//span[text()="上报"]', 300)

    # 现场收方单--选择工程结构
    def receipt_choice(self, bid_name, section_name):
        # 选择相应标段
        time.sleep(5)
        b1 = self.ele.find_ele('xpath', '//input[@placeholder="标段名称"]')
        # ActionChains(self.dr).move_to_element(e).click().perform()
        self.apply_style(b1, '1')
        time.sleep(2)
        b2 = self.ele.find_ele('xpath', '//span[text()="' + bid_name + '"]')
        self.apply_style(b2)
        # 搜索相应的分项工程
        time.sleep(3)
        self.ele.find_ele('id', 'treeSearchKey').send_keys(section_name)
        time.sleep(1)
        b3 = self.ele.find_ele('id', 'treeSearch')
        self.apply_style(b3)
        # 选择分项工程
        time.sleep(2)
        self.ele.find_ele('xpath', '//span[text()="' + section_name+'"]').click()
        time.sleep(0.5)
        self.ele.find_ele('xpath', '//span[text()="' + section_name+'"]/parent::a/preceding-sibling::span[1]').click()
        # elements = self.dr.find_elements_by_class_name('checkbox_false_full')
        # elements[-1].click()
        # self.ele.find_ele('id', 'esTree_4_check').click()

    # 现场收方单--新增-报表数据填写
    # subtitle_list: 为子目号与子目名称中文括号合并后的结果列表
    def receipt_add(self, subtitle_list):
        b1 = self.ele.find_ele('xpath', '//span[text()="新增"]')
        self.apply_style(b1)
        f3 = self.ele.find_ele('xpath', '//div[@class="layui-layer-content"]/iframe')
        self.dr.switch_to.frame(f3)
        time.sleep(1)
        # 新-添加合同清单
        a = -1
        print(subtitle_list)
        for sfd in subtitle_list:
            a += 1
            up_name = sfd['upName']
            item_name = sfd['item_num'] + "（"+sfd['item_name']+"）"
            quantity = sfd['quantity']
            formula = sfd['formula']
            self.ele.find_ele('id', 'treeSearchKey').clear()
            self.ele.find_ele('id', 'treeSearchKey').send_keys(item_name)
            time.sleep(2)
            b2 = self.ele.find_ele('id', 'treeSearch')
            self.apply_style(b2)
            time.sleep(1)
            b3 = self.ele.find_ele('xpath',
                              '//span[text()="'+ up_name + '"]/parent::a/following-sibling::ul//span[text()="'+item_name+'"]//..//../span[2]')
            self.apply_style(b3)
            time.sleep(0.5)
            # 点击添加
            b4 = self.ele.find_ele('xpath', '//span[text()="添加"]')
            self.apply_style(b4)
            time.sleep(1)
            # 填写收方数量
            self.receipt_cell(a, 4).find_element_by_class_name('el-input__inner').send_keys(quantity)
            self.receipt_cell(a, 5).find_element_by_class_name('el-input__inner').send_keys(formula)
            time.sleep(1)
        # 提交
        time.sleep(1)
        b5 = self.ele.find_ele('xpath', '//span[text()="提交"]')
        self.apply_style(b5)

    # 现场收方单--上报审核
    def receipt_upload(self):
        # 点击审批单
        time.sleep(2)
        self.dr.switch_to.parent_frame()
        self.receipt_cell(0, 6).click()
        self.windows_handle()
        # 点击上报
        self.upload_certificate_file()
        time.sleep(5)

    # 更新 收方单的审核状态
    def receipt_state_update(self, fun_name):
        fun_name()

    # 中间计量模块
    # section_name: 分部分项  例： BK0+134.866~BK0+363.755石方路基
    # bid_name: 标段
    def measure_choice(self, bid_name, section_name):
        # 选择相应标段
        time.sleep(3)
        self.ele.find_ele('xpath', '//input[@placeholder="标段名称"]').click()
        self.ele.find_ele('xpath', '//span[text()="' + bid_name + '"]').click()
        # 搜索相应的分项工程
        time.sleep(5)
        self.ele.find_ele('id', 'treeSearchKey').send_keys(section_name)
        time.sleep(1)
        self.ele.find_ele('id', 'treeSearch').click()
        # 选择分项工程
        time.sleep(2)
        self.ele.find_ele('xpath', '//span[text()="' + section_name + '"]').click()

    # 新增中间计量（已收方）
    def measure_increase(self):
        time.sleep(1)
        self.ele.find_ele('xpath', '//span[text()="新增"]').click()
        time.sleep(1)
        # 切换到计量页面iframe
        f1 = self.ele.find_ele('xpath', '//div[@class="layui-layer-content"]/iframe')
        self.dr.switch_to.frame(f1)
        self.ele.find_ele('xpath', '//span[text()="提交"]').click()
        time.sleep(2)

    # 工序检查分部分项工程搜索
    def work_check(self, work_name):
        # 选择已计量
        self.ele.find_ele('class', 'word5').click()
        # 左侧搜索分项工程
        self.ele.find_ele('id', 'treeSearchKey').send_keys(work_name)
        self.ele.find_ele('id', 'treeSearch').click()

    # 工序检查详情查看
    def details_read(self):
        WebDriverWait(self.dr, 30, 0.5).until(ec.visibility_of_element_located((By.XPATH, '//a[text()="查看详情"]')))
        elements = self.dr.find_elements_by_xpath('//a[text()="查看详情"]')
        # 取第一条记录进行详情查看
        elements[0].click()
        time.sleep(1)
        try:
            # 施工自检与监理抽检切换一次
            self.ele.find_ele('xpath', '//div[text()="施工自检"]',2).click()
            time.sleep(3)
            self.ele.find_ele('xpath', '//div[text()="监理抽检"]', 2).click()
        except Exception as e:
            pass

        # 放大一张图片
        WebDriverWait(self.dr, 10, 0.5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'imgs')))
        elements_image = self.dr.find_elements_by_class_name('imgs')
        elements_image[0].click()
        time.sleep(5)
        # 关闭已放大的图片
        elements_image[0].find_element_by_class_name('el-icon-circle-close').click()
        time.sleep(3)
        # 返回到上级iframe
        self.dr.switch_to.parent_frame()
        self.dr.quit()

    # 从业务页面返回到首页页面
    def back_firstpage(self):
        self.ele.find_ele('xpath', '//span[text()="首页"]').click()
        time.sleep(3)

    # BIM融合系统功能
    # wbs结构中跳转到BIM系统中
    def bim_into(self, bid_name, section_name):
        # 选择相应标段
        time.sleep(5)
        b1 = self.ele.find_ele('xpath', '//input[@placeholder="标段名称"]')
        # ActionChains(self.dr).move_to_element(b1).click().perform()
        self.apply_style(b1, '1')
        time.sleep(2)
        b2 = self.ele.find_ele('xpath', '//span[text()="' + bid_name + '"]')
        self.apply_style(b2)
        # 搜索相应的分项工程
        time.sleep(3)
        self.ele.find_ele('id', 'treeSearchKey').send_keys(section_name)
        time.sleep(1)
        b3 = self.ele.find_ele('id', 'treeSearch')
        self.apply_style(b3)

        # # 选择分项工程
        time.sleep(2)
        element1 = self.ele.find_ele('xpath', '//span[text()="'+section_name+'"]')   # 单个
        element2 = self.dr.find_elements_by_xpath('//span[text()="'+section_name+'"]')[0]  # 多个重复
        ActionChains(self.dr).move_to_element(element1).perform()
        time.sleep(1)
        # self.apply_style(element1, '1')
        self.ele.find_ele('class', 'el-icon-map-location').click()
        time.sleep(30)
        #  关闭-重新打开BIM
        self.dr.switch_to.parent_frame()
        self.dr.find_elements_by_class_name('tab-close')[1].click()
        time.sleep(1)
        fs = self.ele.find_ele('xpath', '//div[@id="983761A667A92E12E053E00910ACB0BB"]/iframe')
        self.dr.switch_to.frame(fs)
        time.sleep(1)
        b4 = self.dr.find_elements_by_xpath('//span[text()="' + section_name + '"]')[0]
        # ActionChains(self.dr).move_to_element(element).perform()
        self.apply_style(b4, '1')
        self.ele.find_ele('class', 'el-icon-map-location').click()
        time.sleep(10)
        # 切换到到BIM框架
        self.dr.switch_to.default_content()
        self.dr.switch_to.frame('bim')
        self.dr.switch_to.frame('canvasPaintArea')

    # BIM中数据查看---基础信息
    def bim_data_basic(self):
        self.log.info('>>> BIM-基础信息查看')
        # 查看基础信息
        a1 = self.ele.find_ele('xpath', '//span[text()="基础信息"]', 120)
        self.apply_style(a1)
        try:
            # 设计资料-查看更多
            a2 = self.ele.find_ele('xpath', '//*[text()="设计资料"]//../label', 1)
            if a2.text == '暂无数据':
                self.log.info('>>> 该结构暂无 设计资料')
            else:
                self.apply_style(a2)
                time.sleep(5)
                a3 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a3)
        except Exception as e:
            self.log.info('>>> 该结构 设计资料数据查看 失败')
            pass

    # BIM中数据查看---计量管理
    def bim_data_measure(self):
        self.log.info('>>> BIM-计量管理查看')
        a1 = self.ele.find_ele('xpath', '//span[text()="计量管理"]', 50)
        self.apply_style(a1)
        try:
            # 现场收方单-查看更多
            a2 = self.ele.find_ele('xpath', '//*[text()="现场收方单"]//..//../div[2]/div[last()]', 1)
            if a2.text == '暂无数据':
                self.log.info('>>> 该结构暂无 现场收方单')
            else:
                self.apply_style(a2)
                time.sleep(4)
                a3 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a3)
        except Exception as e:
            self.log.info('>>> 该结构 现场收方单数据查看 失败')
            pass

        try:
            # 计量信息-查看更多
            a4 = self.ele.find_ele('xpath', '//*[text()="计量信息"]//..//../div[2]/div[last()]', 1)
            if a4.text == '暂无数据':
                self.log.info('>>> 该结构暂无 计量信息')
            else:
                self.apply_style(a4)
                time.sleep(4)
                a5 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a5)
        except Exception as e:
            self.log.info('>>> 该结构 计量信息数据查看 失败')
            pass

    # BIM中数据查看---质检评定
    def bim_data_quality(self):
        self.log.info('>>> BIM-质检评定查看')
        a1 = self.ele.find_ele('xpath', '//span[text()="质检评定"]', 10)
        self.apply_style(a1)
        time.sleep(1)
        try:
            # 开工报告--选择一张表单查看
            a2 = self.ele.find_ele('xpath', '//*[text()="开工报告"]//..//../div[2]/div[1]', 3)
            if a2.text == '暂无数据':
                self.log.info('>>> 该结构暂无 开工报告')
            else:
                self.apply_style(a2)
                time.sleep(4)
                a3 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a3)
        except Exception as e:
            self.log.info('>>> 该结构 开工报告数据查看 失败')
            raise e
            pass

        try:
            # 工序检验（施工）-选择一张表单查看
            a4 = self.ele.find_ele('xpath', '//*[text()="工序检验（施工）"]//..//../div[2]/div[1]', 1)
            if a4.text == '暂无数据':
                self.log.info('>>> 该结构暂无 工序检验（施工)')
            else:
                self.apply_style(a4)
                time.sleep(3)
                a5 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a5)
        except Exception as e:
            self.log.info('>>> 该结构 工序检验（施工)数据查看 失败')
            pass

        try:
            # 交工评定（施工）-选择一张表单查看
            a6 = self.ele.find_ele('xpath', '//*[text()="交工评定（施工）"]//..//../div[2]/div[1]', 1)
            if a6.text == '暂无数据':
                self.log.info('>>> 该结构暂无 交工评定（施工)')
            else:
                self.apply_style(a6)
                time.sleep(3)
                a7 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a7)
        except Exception as e:
            self.log.info('>>> 该结构 交工评定（施工)数据查看 失败')
            pass

        try:
            # 工序检验（监理）-选择一张表单查看
            a8 = self.ele.find_ele('xpath', '//*[text()="工序检验（监理）"]//..//../div[2]/div[1]', 1)
            if a8.text == '暂无数据':
                self.log.info('>>> 该结构暂无 工序检验（监理)')
            else:
                self.apply_style(a8)
                time.sleep(3)
                a9 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a9)
        except Exception as e:
            self.log.info('>>> 该结构 工序检验（监理)数据查看 失败')
            pass

        try:
            # 交工评定（监理）-选择一张表单查看
            a10 = self.ele.find_ele('xpath', '//*[text()="交工评定（监理）"]//..//../div[2]/div[1]', 1)
            if a10.text == '暂无数据':
                self.log.info('>>> 该结构暂无 交工评定（监理)')
            else:
                self.apply_style(a10)
                time.sleep(3)
                a11 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a11)
        except Exception as e:
            self.log.info('>>> 该结构 交工评定（监理)数据查看 失败')
            pass

    # BIM中数据查看---工序检查
    def bim_data_process(self):
        self.log.info('>>> BIM-工序检查查看')
        a1 = self.ele.find_ele('xpath', '//span[text()="工序检查"]', 10)
        self.apply_style(a1)
        try:
            # 工序检查--选择一张表单查看
            time.sleep(2)
            a2 = self.dr.find_elements_by_class_name('processContent')[0]
            self.apply_style(a2)
            time.sleep(3)
            a3 = self.ele.find_ele('class', 'ant-modal-close-x')
            self.apply_style(a3)
        except Exception as e:
            self.log.info('>>> 该结构暂无 工序检查')
            pass

    # BIM中数据查看---设计变更
    def bim_data_change(self):
        self.log.info('>>> BIM-设计变更查看')
        a1 = self.ele.find_ele('xpath', '//span[text()="设计变更"]', 10)
        self.apply_style(a1)
        try:
            # 变更信息--选择一张表单查看
            time.sleep(2)
            a2 = self.ele.find_ele('xpath', '//*[text()="变更信息"]//..//../div[2]/div[1]', 2)
            if a2.text == '暂无数据':
                self.log.info('>>> 该结构暂无 变更信息')
            else:
                self.apply_style(a2)
                time.sleep(3)
                a3 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a3)
        except Exception as e:
            self.log.info('>>> 该结构 变更信息数据查看 失败')
            pass

        try:
            # 变更汇总表--选择一张表单查看
            time.sleep(2)
            a4 = self.ele.find_ele('xpath', '//*[text()="变更汇总表"]//..//../div[2]/div[1]', 2)
            if a4.text == '暂无数据':
                self.log.info('>>> 该结构暂无 变更汇总表')
            else:
                self.apply_style(a4)
                time.sleep(3)
                a5 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a5)
        except Exception as e:
            self.log.info('>>> 该结构 变更汇总表数据查看 失败')
            pass

    # BIM中数据查看---进度管理
    def bim_data_progress(self):
        self.log.info('>>> BIM-进度管理查看')
        a1 = self.ele.find_ele('xpath', '//span[text()="进度管理"]', 10)
        self.apply_style(a1)
        try:
            # 年度计划-查看更多
            a2 = self.ele.find_ele('xpath', '//*[text()="年度计划"]//..//../div[2]/div[last()]', 2)
            if a2.text == '暂无数据':
                self.log.info('>>> 该结构暂无 年度计划')
            else:
                self.apply_style(a2)
                time.sleep(3)
                a3 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a3)
        except Exception as e:
            self.log.info('>>> 该结构 年度计划数据查看 失败')
            pass

        try:
            # 进度填报-查看更多
            a4 = self.ele.find_ele('xpath', '//*[text()="进度填报"]//..//../div[2]/div[last()]', 1)
            if a6.text == '暂无数据':
                self.log.info('>>> 该结构暂无 进度填报')
            else:
                self.apply_style(a4)
                time.sleep(3)
                a5 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a5)
        except Exception as e:
            self.log.info('>>> 该结构 进度填报数据查看 失败')
            pass

        try:
            # 形象进度-查看更多
            a6 = self.ele.find_ele('xpath', '//*[text()="形象进度"]//..//../div[2]/div[last()]', 1)
            if a6.text == '暂无数据':
                self.log.info('>>> 该结构暂无 形象进度')
            else:
                self.apply_style(a6)
                time.sleep(3)
                a7 = self.ele.find_ele('class', 'ant-modal-close-x')
                self.apply_style(a7)
        except Exception as e:
            self.log.info('>>> 该结构 形象进度数据查看 失败')
            pass
        self.dr.quit()

# 质检模块功能== == == == 优 == == == == 雅 == ==== == = 的 == ==== == == 分 == == ==== == = 隔 == == == == == == 线 == == == ==

    # 质检评定页面切换
    def quality_page(self, page_name):
        WebDriverWait(self.dr, 10, 0.5).until(
            ec.visibility_of_element_located((By.XPATH, '//li[text()="' + page_name + '"]')))
        self.ele.find_ele('xpath', '//li[text()="' + page_name + '"]').click()

    # 质检评定页面分项工程搜索
    def section_search(self, bid, section_name):
        # 分别选择标段及分项工程信息，查询表单
        time.sleep(8)
        self.ele.find_ele('xpath', '//span[@title="K1"]').click()
        # 选择标段
        time.sleep(2)
        self.ele.find_ele('xpath', '//div[text()="' + bid + '"]').click()
        # 输入分项名称
        time.sleep(2)
        self.ele.find_ele('class', 'ant-input').send_keys(section_name)
        time.sleep(1)  # 防止操作速度超过页面加载速度
        self.ele.find_ele('xpath', '//span[@aria-label="search"]').click()
        self.ele.find_ele('xpath', '//span[text()="' + section_name+'"]').click()
        time.sleep(1)

    # 质检评定页面--添加表单
    def add_main_report(self, main_report_list):   # 传入 主表 列表
        self.ele.find_ele('xpath', '//span[text()="添加表单"]').click()
        for i in main_report_list:
            self.ele.find_ele('xpath', '//div[@class="ant-modal-body"]/div/div/div[2]/div/div/div/div/input').send_keys(i)
            time.sleep(1)
            self.ele.find_ele('xpath', '//div[@class="ant-modal-body"]/div/div/div[2]/div/div/div/div/span').click()
            time.sleep(1)
            self.ele.find_ele('xpath', '//span[text()="' + i + '"]').click()
            time.sleep(1)
            self.ele.find_ele('xpath', '//div[@class="ant-modal-body"]/div/div/div[2]/div/div/div/div/span[2]').click()
            time.sleep(1)
        self.ele.find_ele('xpath', '//span[text()="确 定"]').click()

    # 质检评定页面--添加子表、编辑保存
    # parm1:sub_report  子表列表
    # def add_sub_report(self, sub_report):
    #     row = self.get_report_element(0, 0, alls='2')
    #     row_num = len(row)
    #     for i in range(1, row_num):
    #         # 不需要添加子表的操作
    #         time.sleep(2)  # 判断是否需要添加子表
    #         try:
    #             self.get_report_element(i, 7).find_elements_by_tag_name('button')[1].click()
    #             time.sleep(1)
    #             # 切换到表单编辑页面
    #             time.sleep(3)
    #             self.windows_handle()
    #             # self.ele.find_ele('xpath', '//span[text()="提交"]').click()
    #             # self.ele.find_ele('xpath', '//span[text()="确定"]', 30).click()
    #             self.dr.close()
    #             time.sleep(1)
    #             # 切换回质检评定页面
    #             self.windows_handle()
    #             time.sleep(3)
    #         except Exception as e:
    #             # 需要添加子表--点击查看
    #             self.get_report_element(i, 7).find_elements_by_tag_name('span')[0].click()
    #             time.sleep(1)
    #             # 批量添加
    #             self.ele.find_ele('xpath', '//span[text()="批量添加"]').click()
    #             length_report = len(sub_report)
    #             for j in range(0, length_report):
    #                 report_name = sub_report[j]
    #                 self.dr.find_elements_by_xpath('//input[@placeholder="请输入桩号及工程部位"]')[j].send_keys(report_name)
    #             self.ele.find_ele('xpath', '//span[text()="确 定"]').click()
    #             time.sleep(2)
    #             # 添加完子表后对子表进行编辑及保存
    #             sub_row = self.get_report_element(0, 0, alls='2')
    #             sub_row_num = len(sub_row)
    #             for k in range(1, sub_row_num):
    #                 # 编辑子表
    #                 time.sleep(2)
    #                 self.get_report_element(k, 9).find_elements_by_tag_name('button')[1].click()
    #                 time.sleep(1)
    #                 # 切换到表单编辑页面
    #                 time.sleep(3)
    #                 self.windows_handle()
    #                 # self.ele.find_ele('xpath', '//span[text()="提交"]').click()
    #                 # self.ele.find_ele('xpath', '//span[text()="确定"]', 30).click()
    #                 # 切换回质检评定页面
    #                 self.dr.close()
    #                 time.sleep(1)
    #                 self.windows_handle()
    #                 time.sleep(2)
    #             self.ele.find_ele('xpath', '//span[text()="<返回"]').click()
    #             time.sleep(2)
    #     self.dr.quit()





    # 质检评定页面--批量提交审核

    def add_sub_report(self, sub_report_list):    # 传入 主表：子表 字典
        for main_report in sub_report_list.keys():
            self.ele.find_ele('xpath', '//div[text()="'+main_report+'"]/parent::td/following-sibling::div//span[text()="查看"]').click()
            # 点击批量添加按钮，添加子表
            self.ele.find_ele('xpath', '//span[text()="批量添加"]').click()
            length_report = len(sub_report_list[main_report])
            if length_report >= 8:
                length_report = 8
                for j in range(0, length_report):
                    report_name = sub_report_list[main_report][j]
                    self.dr.find_elements_by_xpath('//input[@placeholder="请输入桩号及工程部位"]')[j].send_keys(report_name)
            self.ele.find_ele('xpath', '//span[text()="确 定"]').click()
            time.sleep(2)
            # 添加完子表后对子表进行编辑及保存
            sub_row = self.get_report_element(0, 0, alls='2')
            sub_row_num = len(sub_row)
            for k in range(1, sub_row_num):
                # 编辑子表
                time.sleep(2)
                self.get_report_element(k, 9).find_elements_by_tag_name('button')[1].click()
                time.sleep(1)
                # 切换到表单编辑页面
                time.sleep(3)
                self.windows_handle()
                # self.ele.find_ele('xpath', '//span[text()="提交"]').click()
                # self.ele.find_ele('xpath', '//span[text()="确定"]', 30).click()
                # 切换回质检评定页面
                self.dr.close()
                time.sleep(1)
                self.windows_handle()
                time.sleep(2)
            self.ele.find_ele('xpath', '//span[text()="<返回"]').click()
            time.sleep(2)


    def auditing_examine(self):
        time.sleep(1)
        self.ele.find_ele('xpath', '//span[text()="一键发起"]').click()
        time.sleep(1)
        elements = self.dr.find_elements_by_xpath('//input[@aria-owns="address_list"]')
        length_elements = len(elements)
        for i in range(length_elements):
            time.sleep(1)
            elements[i].click()
            time.sleep(1)
            self.ele.find_ele('xpath', '//div[text()="系统管理员 乐西管理员1(lxl)"]')
            time.sleep(1)
        self.ele.find_ele('xpath', '//span[text()="确 定"]').click()
        time.sleep(3)
        self.ele.find_ele('xpath', '//span[text()="确 定"]').click()
        self.ele.find_ele('class', 'ant-modal-close-x').click()


# 电子档案模块功能== == == == 优 == == == == 雅 == ==== == = 的 == ==== == == 分 == == ==== == = 隔 == == == == == == 线 == == == ==
    # 文件管理页面归档
    # bid : 标段 ；node_name: 归档节点名称, file_content: 新增文件内容字典
    def file_manage(self, bid, node_name, file_content):
        time.sleep(1)
        self.ele.find_ele('xpath', '//a[text()="文件管理"]', 10).click()
        time.sleep(3)
        self.ele.find_ele('xpath', '//div[@title="K1"]').click()
        time.sleep(1)
        self.ele.find_ele('xpath', '//li[text()="' + bid+'"]').click()
        time.sleep(2)
        self.ele.find_ele('xpath', '//input[@placeholder="请输入关键字"]').send_keys(node_name)
        time.sleep(2)
        self.dr.find_elements_by_class_name('ant-input-suffix')[0].click()  # 点击搜索
        time.sleep(1)
        self.ele.find_ele('xpath', '//span[text()="'+node_name+'"]').click()  # 选中节点值
        time.sleep(1)
        self.ele.find_ele('xpath', '//div[@class="table-header-left"]/div/button[1]').click()  # 点击 新增
        # 新增文件信息
        self.ele.find_ele('xpath', '//textarea[@placeholder="请输入文件题名"]').send_keys(file_content['文件题名'])
        self.ele.find_ele('id', 'serialNumber').send_keys(file_content['文件编号'])
        self.ele.find_ele('name', 'producer').send_keys(file_content['编制单位'])
        self.ele.find_ele('name', 'responsible').send_keys(file_content['责任者'])
        time.sleep(2)
        # 点击保存
        self.ele.find_ele('xpath', '//div[@class="ant-modal-footer"]/div/button[2]').click()



