from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pymysql
import time

def load_hdu(acount,passwd):
    '''
        根据输入的account,passwd来登录，到课程评价页面
    '''
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    chrome_opts = webdriver.ChromeOptions()
    chrome_opts.add_argument('--user-agent=%s' %user_agent)

    browser = webdriver.Chrome(chrome_options=chrome_opts)
    url = 'https://cas.hdu.edu.cn/cas/login'
    browser.get(url)
    is_visible(browser,'//*[@id="un"]')
    name = browser.find_element_by_xpath('//*[@id="un"]')
    name.click()
    name.send_keys(acount)
    pd = browser.find_element_by_xpath('//*[@id="pd"]')
    pd.click()
    pd.send_keys(passwd)
    browser.find_element_by_xpath('//*[@id="index_login_btn"]').click()
    is_visible(browser,'//*[@id="app_a"]/span')
    lgin = browser.find_element_by_xpath('//*[@id="app_a"]/span[text()="选课系统"]')
    lgin.click()
    # 切换到选课系统中
    windows = browser.window_handles
    browser.switch_to.window(windows[1])
    # 判断页面加载完成
    is_visible(browser,'//*[@id="headDiv"]/ul/li[3]/a/span')
    # 鼠标悬停，让选项出现
    lilun = browser.find_element_by_xpath('//*[@id="headDiv"]/ul/li[3]/a/span')
    ActionChains(browser).move_to_element(lilun).perform()
    # 把出现的元素定位，然后点击
    pinjia = browser.find_element_by_xpath('//*[@id="headDiv"]/ul/li[3]/ul/li/a')
    pinjia.click()
    # 开始填写
    tianxie(browser)


def tianxie(browser):
    '''
        在课程评价页面填写表单
    '''
    is_visible(browser,'//*[@id="mainDiv"]')
    browser.switch_to.frame('zhuti')

    # 首先，获取所有课程
    is_visible(browser,'//*[@id="pjkc"]')
    pkjc = browser.find_element_by_xpath('//*[@id="pjkc"]')
    kechens = pkjc.find_elements_by_tag_name("option")
    # 根据课程长度来填写表单
    for k in range(0,len(kechens)):
        is_visible(browser,'//*[@id="DataGrid1_ctl09_JS1"]')
        # 如果有两位老师授课
        if(is_visible2(browser,'//*[@id="DataGrid1"]/tbody/tr[1]/td[5]')):
            for i in range(2,12):
                    if(i<10):
                        xuanxiang = browser.find_element_by_xpath('//*[@id="DataGrid1_ctl0'+str(i)+'_JS1"]')
                        xuanxiang2 = browser.find_element_by_xpath('//*[@id="DataGrid1_ctl0'+str(i)+'_JS2"]')
                    else:
                        xuanxiang = browser.find_element_by_xpath('//*[@id="DataGrid1_ctl'+str(i)+'_JS1"]')
                        xuanxiang2 = browser.find_element_by_xpath('//*[@id="DataGrid1_ctl'+str(i)+'_JS2"]')
                    xuan = Select(xuanxiang)
                    xuan2 = Select(xuanxiang2)
                    if (i==11):
                        xuan.select_by_visible_text('A（非常满意）')
                        xuan2.select_by_visible_text('A（非常满意）')
                        break
                    xuan.select_by_visible_text('B（满意）')
                    xuan2.select_by_visible_text('B（满意）')
        # 只有一位老师授课的情况
        else:
            for i in range(2,12):
                # print(i)
                if(i<10):
                    xuanxiang = browser.find_element_by_xpath('//*[@id="DataGrid1_ctl0'+str(i)+'_JS1"]')
                else:
                    xuanxiang = browser.find_element_by_xpath('//*[@id="DataGrid1_ctl'+str(i)+'_JS1"]')
                xuan = Select(xuanxiang)
                if (i==11):
                    xuan.select_by_visible_text('A（非常满意）')
                    break
                xuan.select_by_visible_text('B（满意）')
        print(k)
        is_visible(browser,'//*[@id="Button1"]')
        save = browser.find_element_by_xpath('//*[@id="Button1"]')
        save.click()
        time.sleep(1)
        alert = browser.switch_to.alert
        alert.accept()


def is_visible(browser,locator, timeout=10):
    '''
        如果页面元素不存在就退出
    '''
    try:
        WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        print('time out')
        exit()

def is_visible2(browser,locator,timeout=5):
    '''
        如果页面元素不存在返回False
    '''
    try:
        WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False


if __name__ == "__main__":
    account = ''
    passwd = ''
    load_hdu(account,passwd)
