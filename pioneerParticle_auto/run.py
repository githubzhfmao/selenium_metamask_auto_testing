import time
import wallet
from config import global_config
import run_checkin_test as checkin
# import muteSwitch_run_test as muteSwitch


wallet_path = global_config.get('path', 'wallet_path').strip()
seed_phrases = wallet.getMnemonic(wallet_path)
result_path = global_config.get('path', 'result_path').strip()
result = open(str(result_path) + 'result.txt', mode='a', encoding='utf-8')

for i in range(1, len(seed_phrases)):

    seed_phrase = seed_phrases[i]
    for j in range(1, 6):
        try:
            checkin.runTest(seed_phrase, 10)
        except Exception:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 第" + str(i) + "次执行失败, 重试次数：" + str(j))
            continue
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 第" + str(i) + "次执行成功")
            break
    print(222222222222222)
