import os.path
import threading
from loguru import logger

logger.add(os.path.join("data", "logs.log"), level="DEBUG", rotation="10 MB", compression="zip")

# пауза между кошельками в секундах от и до, можно не менять
pause = [100, 200]

# перемешивать кошельки?
is_shuffle_wallets = True  # True если перемешивать, False если нет

lock = threading.Lock()

database = os.path.join("data", "database.db")

# включение или выключение квестов
# 1 - квест включен
# 0 - квест выключен
quests_config = {
    'quest_1': 1,  # introduction-to-linea-culture-szn
    'quest_2': 1,  # linea-lxp
    'quest_3': 1,  # nft-learn
    'quest_4': 1,  # how-to-avoid-nft-scams
    'quest_5': 1,  # what-are-metamask-snaps
    'quest_6': 1,  # w1-octomos
    'quest_7': 1,  # w1-crazy-show
    'quest_8': 1,  # w1-push
    'quest_9': 1,  # w1-wizards-of-linea
    'quest_10': 1,  # w1-efrogs
    'quest_12': 1,  # w2-satoshi-universe
    'quest_13': 1,  # w2-linus
    'quest_14': 1,  # w2-yooldo
    'quest_15': 1,  # w2-frog-wars
    'quest_16': 1,  # w2-acg
    'quest_17': 1,  # w2-toad
    'quest_18': 1,  # week-2-voting
    'quest_19': 1,  # w3-ascendtheend-1
    'quest_20': 1,  # w3-sendingme
    'quest_21': 1,  # w3-townstory
    'quest_22': 1,  # w3-danielle-zosavac
    'quest_23': 1,  # w3-demmortal
    'quest_24': 1,  # w3-foxy
    'quest_25': 1,  # week-3-voting
    'quest_26': 1,  # w4-coop-records
    'quest_27': 1,  # w4-borja-moskv
    'quest_28': 1,  # w4-forbidden-fruit
    'quest_29': 1,  # w4-forbidden-fruit-crux
    'quest_30': 1,  # w4-forbidden-fruit-stonez-the-organic
    'quest_31': 1,  # w4-adelaide-laurent-bellue
}
