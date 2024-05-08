import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import datetime
import openpyxl
import requests
import selenium_metamask_automation as auto
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random
import time
import wallet

class Account:
    def __init__(self, address, private_key, mnemonic):
        self.address = address
        self.private_key = private_key
        self.mnemonic = mnemonic

class tokenInfo:
    def __init__(self, address, symbol, name, balance):
        self.address = address
        self.symbol = symbol
        self.name = name
        self.balance = balance



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x600")
        self.master.title("zksync2.0交互")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # 创建导入Excel文件按钮
        self.import_button = tk.Button(self, text="导入Excel文件", command=self.import_excel)
        self.import_button.pack(side="left")

        # 创建查询余额按钮
        self.balance_button = tk.Button(self, text="查询钱包余额", command=self.check_balance)
        self.balance_button.pack(side="left", padx=10)

        # 创建查询余额按钮
        self.balance_button = tk.Button(self, text="syncswap交互", command=self.check_balance)
        self.balance_button.pack(side="left", padx=10)

        # 创建查询余额按钮
        self.balance_button = tk.Button(self, text="mute交互", command=self.opetare_mute)
        self.balance_button.pack(side="left", padx=10)

        # 创建查询余额按钮
        self.balance_button = tk.Button(self, text="zk域名交互", command=self.check_balance)
        self.balance_button.pack(side="left", padx=10)

        self.swap_a_label = tk.Label(root, text="swap_a")
        self.swap_b_label = tk.Label(root, text="swap_b")

        self.swap_a = ttk.Combobox(root, values=["ETH", "USDC"])
        self.swap_b = ttk.Combobox(root, values=["ETH", "USDC"])

        # 设置下拉框默认值
        self.swap_a.current(0)
        self.swap_b.current(0)

        # 显示标签和下拉框
        self.swap_a_label.pack()
        self.swap_a.pack()
        self.swap_b_label.pack()
        self.swap_b.pack()

        # 创建日志输出文本框
        self.log_text = tk.Text(self.master, width=400, height=500)
        self.log_text.pack(pady=20)
        self.log_text.configure(state='disabled')


    def import_excel(self):
        try:
            # 弹出文件选择窗口，选择Excel文件
            file_path = filedialog.askopenfilename()
            self.log("导入Excel文件：%s" % file_path)
            # 读取Excel文件中的数据
            wb = openpyxl.load_workbook(file_path)
            ws = wb.active
            rows = ws.iter_rows(min_row=2)
            self.accounts = []
            for row in rows:
                address = row[0].value
                private_key = row[1].value
                mnemonic = row[2].value
                account = Account(address, private_key, mnemonic)
                self.accounts.append(account)
            self.log("导入Excel文件完成，共%d个账号" % len(self.accounts))
        except Exception as e:
            self.log(f"Error: {str(e)}")


    def opetare_mute(self):
        for account in self.accounts:
            self.log(account.address + ":开始操作")
            driver = auto.launchSeleniumWebdriver("/Users/paul/Desktop/testzksync/chromedriver")
            driver.implicitly_wait(5)
            # 打开https://app.mute.io/准备交互
            driver.get('https://app.mute.io/')
            password = '12345678'
            auto.metamaskSetup(account.mnemonic, password)
            auto.changeNetworkByChainList("zkSync Era Mainnet")
            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="app"]/header[1]/div[4]/button').click()
            driver.find_element(By.XPATH, "//button[text()='Metamask (injected)']").click()
            # 连接钱包
            auto.connectToWebsite('//button[text()="下一步"]')
            self.log(account.address + ":开始swap操作")
            token_x = self.swap_a.get()
            token_y = self.swap_b.get()
            for key, value in self.allAddressDict.items():
                for key1, value1 in value.items():
                    print(key, value)
                    if key1 == token_x:
                        buttons = driver.find_elements(By.XPATH, "//button[text()='Select token']")
                        buttons[0].click()
                        time.sleep(3)
                        driver.find_element(By.XPATH, "//p[text()='" + token_x + "']").click()
                        buttons[1].click()
                        time.sleep(3)
                        driver.find_element(By.XPATH, "//p[text()='" + token_y + "']").click()
                        inputs = driver.find_elements(By.XPATH, '//input')
                        value = random.uniform(value1.balance / 10, value1.balance)
                        value = format(value, '.5f')
                        inputs[0].send_keys(value)
                        time.sleep(3)
                        while True:
                            try:
                                driver.find_element(By.XPATH, '//button[text()="Swap"]').click()
                                auto.confirmApprovalFromMetamask()
                                time.sleep(5)
                                # if token_y == 'ETH':
                                #     driver.find_element(By.XPATH, '//button[text()="Approve"]').click()
                                #     auto.confirmApprovalFromMetamask()
                                # else:
                                #     # element = driver.find_element(By.XPATH, '//button[text()="Approve"]')
                                #
                                # auto.confirmApprovalFromMetamask()
                                self.log(account.address + "结束swap操作")
                                break
                            except NoSuchElementException:
                                break
                                self.log(account.address + "swap操作错误")
                        time.sleep(15)

                    # 进行pool操作
            driver.refresh()
            driver.find_element(By.XPATH, '//a[text()="Pool"]').click()
            driver.find_element(By.XPATH, '//button[text()="Add Liquidity"]').click()
            buttons = driver.find_elements(By.XPATH, "//button[text()='Select token']")
            buttons[0].click()
            time.sleep(3)
            driver.find_element(By.XPATH, "//p[text()='" + token_x + "']").click()
            buttons[1].click()
            time.sleep(3)
            driver.find_element(By.XPATH, "//p[text()='" + token_y + "']").click()
            time.sleep(3)
            driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/button").click()
            time.sleep(1)
            inputs = driver.find_elements(By.XPATH, '//input')
            self.check_balance_addrsss(account.address)
            value = random.uniform(self.addressBalance[token_x] / 10, self.addressBalance[token_x].balance)
            value = format(value, '.5f')
            inputs[0].send_keys(value)
            driver.find_element(By.XPATH, '//button[text()="Add liquidity"]').click()
            auto.confirmApprovalFromMetamask()
            # value = random.uniform(self.addressBalance[token_y] / 10, self.addressBalance[token_y].balance)
            # value = format(value, '.5f')
            # inputs[0].send_keys(value)
            # value = random.uniform(value1.balance / 10, value1.balance)
            # value = format(value, '.5f')
            # inputs[0].send_keys(value)
            driver.quit();








    def check_balance(self):
        base_url = "https://zksync2-mainnet-explorer.zksync.io/address"
        self.balances_list = []
        self.addressDict = {}
        self.allAddressDict = {}
        for account in self.accounts:
            address = account.address
            url = f"{base_url}/{address}"
            response = requests.get(url)
            data = response.json()
            allBalance = data["info"]["balances"]
            for key, value in allBalance.items():
                balance = int(value["balance"], 16)
                balance = balance / (10 ** value["tokenInfo"]['decimals'])
                token_info = tokenInfo(value["tokenInfo"]['address'], value["tokenInfo"]['symbol'],value["tokenInfo"]['name'],balance)
                self.addressDict[value["tokenInfo"]['symbol']] = token_info
            self.allAddressDict[address] = self.addressDict

        self.log("所有账号都完成了余额查询，可以进行下一步了")

    def check_balance_addrsss(self, address):
        base_url = "https://zksync2-mainnet-explorer.zksync.io/address"
        url = f"{base_url}/{address}"
        self.addressBalance = {}
        response = requests.get(url)
        data = response.json()
        allBalance = data["info"]["balances"]
        for key, value in allBalance.items():
            balance = int(value["balance"], 16)
            balance = balance / (10 ** value["tokenInfo"]['decimals'])
            self.addressBalance[value["tokenInfo"]['symbol']] = balance



    def log(self, message):
        # 记录日志
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = "[%s] %s\n" % (current_time, message)
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert("end", log_message)
        self.log_text.see("end")

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
