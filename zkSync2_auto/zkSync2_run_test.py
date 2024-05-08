import selenium_metamask_automation as auto
import time
import wallet
import random
from config import global_config
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def runTest(addr,wait_time):
    # 指定chromedriver路径
    driver_path = global_config.get('path', 'driver_path').strip()
    driver = auto.launchSeleniumWebdriver(driver_path)
    driver.implicitly_wait(wait_time)
    # 打开https://app.mute.io/准备交互
    # driver.get('https://app.mute.io/')
    # time.sleep(10)
    # address = addr
    # seed_phrase = wallet.getSeedPhraseV2(address)
    # password = 'alameda1508'
    # # 导入助记词
    # auto.metamaskSetup(seed_phrase, password)
    # # network_name = 'Goerli 测试网络'
    # # # 切换到测试网络
    # # auto.changeMetamaskNetwork(network_name)
    # auto.changeNetworkByChainList("zkSync Era Mainnet")
    # driver.switch_to.window(driver.window_handles[0])
    # driver.refresh()
    # time.sleep(5)
    # driver.find_element(By.XPATH, '//*[@id="app"]/header[1]/div[4]/button').click()
    # driver.find_element(By.XPATH, "//button[text()='Metamask (injected)']").click()
    # # 连接钱包
    # auto.connectToWebsite('//button[text()="下一步"]')
    #
    # token_x = 'ETH'
    # token_y = 'WETH'
    # buttons = driver.find_elements(By.XPATH, "//button[text()='Select token']")
    # buttons[0].click()
    # driver.find_element(By.XPATH, "//p[text()='" + token_x + "']").click()
    # buttons[1].click()
    # driver.find_element(By.XPATH, "//p[text()='" + token_y + "']").click()
    # inputs = driver.find_elements(By.XPATH,'//input')
    #
    # value = random.uniform(0.0001,0.001)
    # value = format(value, '.5f')
    # inputs[0].send_keys(value)
    #
    # if token_x != 'ETH':
    #
    #
    #     while True:
    #         try:
    #             element = driver.find_element(By.XPATH,'//button[text()="Approve"]')
    #         except NoSuchElementException:
    #             print("Swap")
    #             driver.find_element(By.XPATH,'//button[text()="Swap"]').click()
    #             auto.signConfirm()
    #             driver.find_element(By.XPATH,"//*[@alt='Close']").click()
    #             break
    #         else:
    #             print("Approve")
    #             driver.find_element(By.XPATH,'//button[text()="Approve"]').click()
    #             auto.signConfirm()
    #             auto.signConfirm()
    #             driver.find_element(By.XPATH,"//*[@alt='Close']").click()
    #             break
    #     print('run swap success')
    # else:
    #     driver.find_element(By.XPATH, "//button[text()='Wrap ETH']").click()
    #
    # auto.confirmApprovalFromMetamask()

    # 交互https://syncswap.xyz/
    driver.get('https://syncswap.xyz/')
    time.sleep(10)
    driver.find_element(By.XPATH, "//button[text()='Connect").click()
    driver.find_element(By.XPATH, "//p[text()='Ethereum Wallet']").click()
    # 连接钱包
    auto.connectToWebsite('//button[text()="下一步"]')



    # 退出
    screenshot_path = global_config.get('path', 'result_path').strip()
    driver.quit()
