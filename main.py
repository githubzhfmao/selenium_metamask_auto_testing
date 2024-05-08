from tkinter import *
import time
import wallet
# from config import global_config
# import zkSync2_auto.zkSync2_run_test as zkSync
from tkinter import filedialog
import selenium_metamask_automation as auto
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random

import wallet


def importExcel():
    global wallets
    global address_list
    global filename
    filename = filedialog.askopenfilename()
    wallets = wallet.getWallet(filename)
    address_list = wallets[0]




def runMute(addr,wait_time,driver_path):
    # 指定chromedriver路径
    global driver
    driver = auto.launchSeleniumWebdriver(driver_path)
    driver.implicitly_wait(wait_time)
    # 打开https://app.mute.io/准备交互
    driver.get('https://app.mute.io/')
    time.sleep(10)
    address = addr
    seed_phrase = wallet.getSeedPhraseV2(address,filename)
    password = 'alameda1508'
    # 导入助记词
    auto.metamaskSetup(seed_phrase, password)
    # network_name = 'Goerli 测试网络'
    # # 切换到测试网络
    # auto.changeMetamaskNetwork(network_name)
    auto.changeNetworkByChainList("zkSync Era Mainnet")
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="app"]/header[1]/div[4]/button').click()
    driver.find_element(By.XPATH, "//button[text()='Metamask (injected)']").click()
    # 连接钱包
    auto.connectToWebsite('//button[text()="下一步"]')

    token_x = 'ETH'
    token_y = 'WETH'
    buttons = driver.find_elements(By.XPATH, "//button[text()='Select token']")
    buttons[0].click()
    driver.find_element(By.XPATH, "//p[text()='" + token_x + "']").click()
    buttons[1].click()
    driver.find_element(By.XPATH, "//p[text()='" + token_y + "']").click()
    inputs = driver.find_elements(By.XPATH,'//input')

    value = random.uniform(0.0001,0.001)
    value = format(value, '.5f')
    inputs[0].send_keys(value)

    if token_x != 'ETH':


        while True:
            try:
                element = driver.find_element(By.XPATH,'//button[text()="Approve"]')
            except NoSuchElementException:
                print("Swap")
                driver.find_element(By.XPATH,'//button[text()="Swap"]').click()
                auto.signConfirm()
                driver.find_element(By.XPATH,"//*[@alt='Close']").click()
                break
            else:
                print("Approve")
                driver.find_element(By.XPATH,'//button[text()="Approve"]').click()
                auto.signConfirm()
                auto.signConfirm()
                driver.find_element(By.XPATH,"//*[@alt='Close']").click()
                break
        print('run swap success')
    else:
        driver.find_element(By.XPATH, "//button[text()='Wrap ETH']").click()

    auto.confirmApprovalFromMetamask()
    time.sleep(15)
    driver.quit()


def doubleRunMute():
    rows = wallet.Excel(filename).getRows()
    for i in range(1, rows):
        runMute(address_list[i], 10, inp1.get())


def runZkNames(addr,driver_path):
    driver = auto.launchSeleniumWebdriver(driver_path)
    driver.implicitly_wait(10)
    # 打开https://app.mute.io/准备交互
    driver.get('https://app.zkns.domains/')
    time.sleep(5)

    address = addr
    seed_phrase = wallet.getSeedPhraseV2(address, filename)
    password = 'alameda1508'
    # 导入助记词
    auto.metamaskSetup(seed_phrase, password)
    # network_name = 'Goerli 测试网络'
    # # 切换到测试网络
    # auto.changeMetamaskNetwork(network_name)
    auto.changeNetworkByChainList("zkSync Era Mainnet")
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    time.sleep(5)

    driver.find_element(By.XPATH, "//button[text()='Connect Wallet']").click()
    driver.find_element(By.XPATH, "//div[text()='Connect to MetaMask wallet']").click()
    # 连接钱包
    auto.connectToWebsite('//button[text()="下一步"]')
    driver.refresh()
    time.sleep(5)
    inputs = driver.find_elements(By.XPATH, '//input')

    value = random.randint(100000, 10000000)
    inputs[0].send_keys(value)

    driver.find_element(By.XPATH, "//button[text()='Search']").click()
    driver.find_element(By.XPATH, "//div[text()='Available']").click()
    driver.find_element(By.CLASS_NAME, "sc-eYmodA bsYfAj").click()

    auto.confirmApprovalFromMetamask()
    time.sleep(15)
    driver.quit()


def doubleRunZkNames():
    rows = wallet.Excel(filename).getRows()
    for i in range(1, rows):
        runZkNames(address_list[i],inp1.get())


root = Tk()
lb_1=Label(root,text="请输入你的谷歌浏览器的chromedriver位置后开始操作")
lb_1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

inp1 = Entry(root)
inp1.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)

btn1 = Button(root, text='导入需要操作的账号', command=importExcel)
btn1.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.1)

btn1 = Button(root, text='mute交互', command=doubleRunMute)
btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)


btn3 = Button(root, text='zk 域名', command=doubleRunZkNames)
btn3.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.1)


btn3 = Button(root, text='mintsquare交互')
btn3.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.1)

btn2 = Button(root, text='syncswap交互')
btn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)



# 创建一个文本框用来显示计算得到的结果
txt = Text(root)
txt.place(relx=0.1, rely=0.8, relheight=0.3)

root.geometry('800x400')
root.title('zksync2.0交互')
root.mainloop()
