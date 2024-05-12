import time
import wallet
from config import global_config
import run_swap_single_handler as swap


wallet_path = global_config.get('path', 'wallet_path').strip()
seed_phrases = wallet.getMnemonic(wallet_path)
result_path = global_config.get('path', 'result_path').strip()
result = open(str(result_path) + 'result.txt', mode='a', encoding='utf-8')
target_wallets = wallet.getWallet('targetwallet.xlsx')[0]
for j in range(1, 121):
    for i in range(1, len(seed_phrases)):

        seed_phrase = seed_phrases[i]
        try:
            swap.runTest(seed_phrase, 10, target_wallets)
        except Exception as e:
            print(e)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 第" + str(i) + "个钱包 第" + str(j) + "次执行失败")
            continue
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 第" + str(i) + "次执行成功")
        print(222222222222222)
