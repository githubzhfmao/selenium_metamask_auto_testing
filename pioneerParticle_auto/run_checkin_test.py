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
    password = 'Aa112211'
    # 导入助记词
    auto.metamaskSetup(seed_phrase, password)
    driver.implicitly_wait(wait_time)

    auto.driverClick(By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[3]/div[4]/button[1]/div[1]/div/span")
    time.sleep(2)
    # 连接钱包
    auto.connectToWebsite('//button[text()="下一步"]')
    time.sleep(2)
    auto.signin()
    time.sleep(2)
    auto.driverClick(By.XPATH, '//*[@id="navbar"]/header/ul[2]/li[1]/a')
    checkin_flag = auto.driverClick(By.XPATH, '//button[div[div[span[text()="Check-in"]]]]')
    if checkin_flag:

        conform = auto.driverClick(By.XPATH, '//button[div[div[span[div[text()="Confirm"]]]]]')
        if conform:
            auto.acceptNetworkByChain('//button[text()="批准"]')
            checkin_flag = auto.driverClick(By.XPATH, '//button[div[div[span[div[text()="Confirm"]]]]]')
            if checkin_flag:
                time.sleep(2)
                auto.signin(2)
                time.sleep(5)
        else:

            # deposit = auto.driverClick(By.XPATH, '//button[div[div[span[text()="Deposit"]]]]')
            # if deposit:
            #     input_eth = driver.find_element(By.XPATH,
            #                                     "/html/body/div[1]/div[1]/div/div[1]/div/div[1]/div[3]/div[2]/div[1]/input")
            #     input_eth.send_keys("0.1")
            #     auto.driverClick(By.XPATH, '//button[div[div[span[text()="Deposit Universal Gas"]]]]')
            #     time.sleep(2)
            #     auto.depositNetworkByChain()
            #     time.sleep(2)
            #     auto.driverClick(By.XPATH, '//*[@id="navbar"]/header/ul[2]/li[1]/a')
            #     checkin_flag = auto.driverClick(By.XPATH, '//button[div[div[span[text()="Check-in"]]]]')
            #     if checkin_flag:
            #
            #         conform = auto.driverClick(By.XPATH, '//button[div[div[span[div[text()="Confirm"]]]]]')
            #         if conform:
            #             auto.acceptNetworkByChain('//button[text()="批准"]')
            #             checkin_flag = auto.driverClick(By.XPATH, '//button[div[div[span[div[text()="Confirm"]]]]]')
            #             if checkin_flag:
            #                 time.sleep(2)
            #                 auto.signin(2)
            #                 time.sleep(5)
            # else:
            print("今日已签到")
    else:
        print("今日已签到")
    # # 退出
    # screenshot_path = global_config.get('path', 'result_path').strip()
    # driver.quit()
