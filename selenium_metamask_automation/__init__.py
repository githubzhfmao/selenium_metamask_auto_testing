from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import os
import urllib.request
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

EXTENSION_PATH = os.path.abspath(r"..") + '/selenium_metamask_auto_testing/selenium_metamask_automation/extension_metamask.crx'

EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'


def downloadMetamaskExtension():
    print('Setting up metamask extension please wait...')

    url = 'https://xord-testing.s3.amazonaws.com/selenium/10.0.2_0.crx'
    urllib.request.urlretrieve(url, os.getcwd() + '/extension_metamask.crx')


def launchSeleniumWebdriver(driverPath):
    print('path', EXTENSION_PATH)
    chrome_options = Options()
    chrome_options.add_extension(EXTENSION_PATH)
    global driver
    driver = webdriver.Chrome(options=chrome_options, executable_path=driverPath)
    # time.sleep(5)
    print("Extension has been loaded")
    return driver

def launchSeleniumWebdriver2(driverPath, extensionPath):
    print('path', extensionPath)
    chrome_options = Options()
    chrome_options.add_extension(extensionPath)
    global driver
    driver = webdriver.Chrome(options=chrome_options, service=Service(driverPath))
    # time.sleep(5)
    print("Extension has been loaded")
    return driver

def checkHandles():
    handles_value = driver.window_handles
    if len(handles_value) > 1:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        checkHandles()


def metamaskSetup(recoveryPhrase, password):

    driver.switch_to.window(driver.window_handles[1])
    driverClick(By.ID, 'onboarding__terms-checkbox')
    driverClick(By.XPATH, '//button[text()="导入现有钱包"]')
    driverClick(By.XPATH, '//button[text()="我同意"]')

    phrases = recoveryPhrase.split(" ")
    if len(phrases) == 24:
        driverClick(By.CLASS_NAME, 'dropdown__select')
        time.sleep(2)
        driverClick(By.XPATH, '//option[text()="我有一个包含24个单词的私钥助记词"]')
        time.sleep(2)
    elif len(phrases) != 12:
        raise ValueError(f'助记词长度异常：{len(phrases)}')

    inputs = driver.find_elements(By.CLASS_NAME, 'MuiInputBase-input')
    i = 0
    for phrase in phrases:
        inputs[i].send_keys(phrase)
        i += 1

    driverClick(By.XPATH, '//button[text()="确认私钥助记词"]')

    inputs = driver.find_elements(By.XPATH, '//input')
    inputs[0].send_keys(password)
    inputs[1].send_keys(password)
    driverClick(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input')
    driverClick(By.XPATH, '//button[text()="导入我的钱包"]')
    driverClick(By.XPATH, '//button[text()="知道了！"]')
    driverClick(By.XPATH, '//button[text()="下一步"]')
    driverClick(By.XPATH, '//button[text()="完成"]')
    # time.sleep(2)

    # # closing the message popup after all done metamask screen
    # driverClick(By.XPATH,'//*[@id="popover-content"]/div/div/section/header/div/button')
    # time.sleep(2)
    print("Wallet has been imported successfully")
    # time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def driverClick(by: By, value: str, cnt=4) -> bool:
    for i in range(1, cnt):
        try:
            driver.find_element(by, value).click()
        except Exception as e:
            print(f"第{i}次点击失败：{value}")
            time.sleep(2)
        else:
            return True
    return False

def changeMetamaskNetwork(networkName):
    # opening network
    print("Changing network")
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    driverClick(By.XPATH,'//*[@id="popover-content"]/div/div/section/header/div/button')
    # 打开网络下拉框
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span')
    # 跳转开启测试网设置
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[2]/div/div[1]/div[3]/span/a')
    # 显示测试网
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]/div[2]/div')
    # 滑到最上方
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    # 打开网络下拉框
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span')
    print("opening network dropdown")
    time.sleep(2)
    # 以太坊 Ethereum 主网络
    # Ropsten 测试网络
    # Kovan 测试网络
    # Rinkeby 测试网络
    # Goerli 测试网络
    all_li = driver.find_elements(By.TAG_NAME,'li')

    for li in all_li:
        text = li.text
        if text == networkName:
            li.click()
            print(text, "is selected")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return
    print("Please provide a valid network name")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


def addAndChangeNetwork():
    time.sleep(5)
    print("添加并切换网络开始")
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    # driver.refresh()
    driverClick(By.XPATH,"//button[text()='批准']")
    driverClick(By.XPATH,"//button[text()='切换网络']")
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def changeNetworkByChainList(network_name):
    """
    通过Chainlist.org切换指定网络

    :Args:
        - network_name: string 完整的网络名.

    :Usage:
        auto.changeNetworkByChainList('Binance Smart Chain Mainnet')
    """
    time.sleep(5)
    print("切换指定网络开始")
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://chainlist.org/')
    driverClick(By.XPATH,"//button[text()='Connect Wallet']")
    # connect chainlist
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driverClick(By.XPATH,'//button[text()="下一步"]')
    driverClick(By.XPATH,'//button[text()="连接"]')
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    # search Network
    # driverClick(By.XPATH,"//span[text()='Testnets']")
    time.sleep(1)
    inputs = driver.find_elements(By.XPATH,'//input') [1,2,3]
    inputs[0].send_keys(network_name)
    time.sleep(1)
    driverClick(By.XPATH,"//button[text()='Add to Metamask']")
    # change Network
    time.sleep(3)
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[2])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    driverClick(By.XPATH,"//button[text()='批准']")
    driverClick(By.XPATH,"//button[text()='切换网络']")
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def connectToWebsite(str):
    time.sleep(2)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(2)
    driverClick(By.XPATH,str)
    driverClick(By.XPATH,'//button[text()="连接"]')
    print('Site connected to metamask')
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def acceptNetworkByChain(str):
    time.sleep(2)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")

    time.sleep(2)
    driverClick(By.XPATH, str)
    driverClick(By.XPATH,'//button[text()="切换网络"]')
    print('Site connected to metamask')
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def signin(cnt=0):

    time.sleep(2)
    driver.execute_script("window.open('');")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driverClick(By.XPATH, '//button[text()="明白了！"]', cnt)
    driverClick(By.XPATH, '//button[text()="签名"]')
    print('Site signin to metamask')
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def confirmApprovalFromMetamask():
    time.sleep(10)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    driverClick(By.XPATH,'//button[text()="确认"]')
    print("Approval transaction confirmed")

    driver.close()
    # switch back
    driver.switch_to.window(driver.window_handles[0])


def rejectApprovalFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    # time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    # time.sleep(10)
    # confirm approval from metamask
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[1]')
    time.sleep(8)
    print("Approval transaction rejected")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    print("Reject approval from metamask")


def confirmTransactionFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(10)

    # # confirm transaction from metamask
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]')
    time.sleep(13)
    print("Transaction confirmed")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(3)


def rejectTransactionFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(5)
    # confirm approval from metamask
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[1]')
    time.sleep(2)
    print("Transaction rejected")

    # switch to web window
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

def addToken(tokenAddress):
    # opening network
    print("Adding Token")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    print("closing popup")
    time.sleep(5)
    driverClick(By.XPATH,'//*[@id="popover-content"]/div/div/section/header/div/button')

    # driverClick(By.XPATH,'//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span')
    # time.sleep(2)

    print("clicking add token button")
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[4]/div/div/div/div[3]/div/div[3]/button')
    time.sleep(2)
    # adding address
    driver.find_element_by_id("custom-address").send_keys(tokenAddress)
    time.sleep(10)
    # clicking add
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[4]/div/div[2]/div[2]/footer/button[2]')
    time.sleep(2)
    # add tokens
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[4]/div/div[3]/footer/button[2]')
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


def signConfirm():
    time.sleep(5)
    checkHandles()
    time.sleep(1)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(5)
    while True:
        try:
            element = driverClick(By.XPATH,'//*[@id="app-content"]/div/div[2]/div/div[3]/div[1]')
        except NoSuchElementException:
            time.sleep(1)
            print('签名了，但没有完全签名')
            break
        else:
            driverClick(By.XPATH,'//*[@id="app-content"]/div/div[2]/div/div[3]/div[1]')
            driverClick(By.XPATH,'//button[text()="签名"]')
            time.sleep(1)
            print('签名完成')
            break
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def signReject():
    print("sign")
    time.sleep(3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driverClick(By.XPATH,'//*[@id="app-content"]/div/div[3]/div/div[3]/button[1]')
    time.sleep(1)
    # driverClick(By.XPATH,'//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]')
    # time.sleep(3)
    print('Sign rejected')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
