import selenium_metamask_automation as auto
import time
import wallet
import random
from config import global_config
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def runTest(seed_phrase, wait_time):
    # 指定chromedriver路径
    driver_path = global_config.get('path', 'driver_path').strip()
    metamask_path = global_config.get('path', 'metamask_path').strip()
    driver = auto.launchSeleniumWebdriver2(driver_path, metamask_path)

    # 登录页面 https://pioneer.particle.network/zh-CN/signup
    driver.get('https://pioneer.particle.network/zh-CN/signup')
    driver.implicitly_wait(wait_time)
    password = 'Aa112211'
    # 导入助记词
    auto.metamaskSetup(seed_phrase, password)

    auto.driverClick(By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[3]/div[4]/button[1]/div[1]/div/span")
    # 连接钱包
    auto.connectToWebsite('//button[text()="下一步"]')

    driver.get('https://pioneer.particle.network/zh-CN/point')
    driver.implicitly_wait(wait_time)
    auto.signin()
    checkin_flag = auto.driverClick(By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div/div[4]/div[4]/button/div[1]/div/span")
    if checkin_flag:
        auto.driverClick(By.XPATH, "/html/body/div[4]/div/div[2]/div/div/div[2]/div[4]/div[2]/button/div[1]/div/span/div")
        auto.acceptNetworkByChain('//button[text()="批准"]')
        auto.signin(3)
        time.sleep(5)
    else:
        print("今日已签到")
    # # 退出
    # screenshot_path = global_config.get('path', 'result_path').strip()
    # driver.quit()
