from selenium.common import NoSuchElementException

import selenium_metamask_automation as auto
import time
import wallet
import random
from config import global_config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def wait_for_document(driver):
    time.sleep(3)
    for i in range(20):
        if driver.execute_script("return document.readyState") == "complete":
            return
        else:
            time.sleep(1)


def runTest(seed_phrase, wait_time, target_wallets):
    start = time.perf_counter()
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
    for i in range(5):
        auto.driverClick(By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[3]/div[4]/button[1]/div[1]/div/span")
        # 连接钱包
        click = auto.connectToWebsite('//button[text()="下一步"]')
        time.sleep(2)
        if click:
            auto.signin()
            time.sleep(2)
            break
    auto.driverClick(By.XPATH, '//*[@id="navbar"]/header/ul[2]/li[1]/a')
    aa_wallet = auto.driverClick(By.XPATH, "/html/body/div[3]/button/img[1]")
    if aa_wallet:
        auto.switchNetworkByChain()
        time.sleep(2)
        iframe_start = time.perf_counter()
        WebDriverWait(driver, 20).until(ec.frame_to_be_available_and_switch_to_it("particle-auth-core-iframe-wallet"))

        send_xpath = '//*[@id="keep-alive-container"]/div/div/div/div[2]/div[1]/div[4]/div[1]/div'
        for i in range(20):
            auto.driverClick(By.XPATH, send_xpath, 1)
            time.sleep(1)
            try:
                driver.find_element(By.XPATH, '//*[@id="send_to"]')
            except NoSuchElementException:
                continue
            else:
                break
        print("切换iframe", time.perf_counter() - iframe_start, "秒")
        to_addr = driver.find_element(By.XPATH, '//*[@id="send_to"]')
        to_addr.clear()
        to_addr.send_keys(target_wallets[random.randint(1, len(target_wallets))])

        amount = driver.find_element(By.XPATH, '//*[@id="send_amount"]')
        amount.clear()
        amount.send_keys('0.00000001')
        auto.driverClick(By.XPATH, '//*[@id="send"]/div[4]/div/div/div/div/button')
        for i in range(5):
            time.sleep(2)
            auto.driverClick(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div[2]/div/div[2]/button', 1)
            if len(driver.window_handles) > 1:
                break
        auto.signin()
        time.sleep(2)
        driver.switch_to.frame("particle-auth-core-iframe-wallet")
        for i in range(20):
            try:
                driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[2]/div/div[3]/button/span[2]')
            except NoSuchElementException:
                time.sleep(1)
                continue
            else:
                break
        # 获取结束时间
        end = time.perf_counter()
        # 计算运行时间
        print("运行时间：", end - start, "秒")
    else:
        print("AA钱包加载失败")
    # # 退出
    # screenshot_path = global_config.get('path', 'result_path').strip()
    # driver.quit()
