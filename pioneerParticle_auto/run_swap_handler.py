import selenium_metamask_automation as auto
import time
import wallet
import random
from config import global_config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


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

    auto.driverClick(By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[3]/div[4]/button[1]/div[1]/div/span")
    # 连接钱包
    auto.connectToWebsite('//button[text()="下一步"]')
    time.sleep(2)
    auto.signin()
    time.sleep(2)
    auto.driverClick(By.XPATH, '//*[@id="navbar"]/header/ul[2]/li[1]/a')
    aa_wallet = auto.driverClick(By.XPATH, "/html/body/div[3]/button/img[1]")
    if aa_wallet:
        auto.switchNetworkByChain()
        time.sleep(2)

        while True:
            try:
                driver.switch_to.frame("particle-auth-core-iframe-wallet")
                success_num = 0
                error_num = 0
                time.sleep(20)
                send_xpath = '//*[@id="keep-alive-container"]/div/div/div/div[2]/div[1]/div[4]/div[1]/div'
                auto.driverClick(By.XPATH, send_xpath, 20)
                time.sleep(4)
                to_addr = driver.find_element(By.XPATH, '//*[@id="send_to"]')
                to_addr.clear()
                to_addr.send_keys(target_wallets[random.randint(1, len(target_wallets))])

                time.sleep(2)
                amount = driver.find_element(By.XPATH, '//*[@id="send_amount"]')
                amount.clear()
                amount.send_keys('0.00000001')
                time.sleep(4)
                auto.driverClick(By.XPATH, '//*[@id="send"]/div[4]/div/div/div/div/button')
                time.sleep(4)
                auto.driverClick(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div[2]/div/div[2]/button')
                time.sleep(4)
                auto.driverClick(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div[2]/div/div[2]/button')
                auto.signin()
                time.sleep(20)
                success_num += 1
            except Exception as e:
                error_num += 1
                print(e)
                if error_num > 100:
                    break
            else:
                if success_num > 100:
                    break
            finally:
                driver.refresh()
                time.sleep(20)
                auto.driverClick(By.XPATH, "/html/body/div[3]/button/img[1]")
        # 获取结束时间
        end = time.perf_counter()
        # 计算运行时间
        print("运行时间：", end - start, "秒")
    else:
        print("AA钱包加载失败")
    # # 退出
    # screenshot_path = global_config.get('path', 'result_path').strip()
    # driver.quit()
