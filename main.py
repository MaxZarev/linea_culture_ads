import random

from classes.client import Linea
from classes.database import Database
from config import logger, is_shuffle_wallets


def worker(profile) -> None:
    try:
        client = Linea(profile)
        try:
            client.run_quests()
        except Exception as ex:
            logger.error(f"Error inside in profile {profile}: {ex}")
        finally:
            client.profile_close()
    except Exception as ex:
        logger.error(f"Error outside in profile {profile}: {ex}")



def main():
    message = ("1. Создать или пересоздать базу данных\n"
               "2. Запуск квестов для незавершенных профилей\n"
               "3. Запустить отдельный профиль\n"
               "4. Напечатать результаты работы\n"
               "5. Сбросить статусы у квеста, чтобы пройти его повторно на всех профилях\n")


    answer = input(f"{message}: ")
    if answer == "1":
        Database.create_database()
    elif answer == "2":
        Database.update_database()
        profiles = Database.get_profiles()
        if is_shuffle_wallets:
            random.shuffle(profiles)
        for profile in profiles:
            worker(profile)
    elif answer == "3":
        profile = input("Введите номер профиля: ")
        worker(int(profile))
    elif answer == "4":
        Database.print_database()
    elif answer == "5":
        quest_number = input("Введите номер квеста числом (смотрите в config): ")
        Database.reset_quest_status(quest_number)



if __name__ == '__main__':
    main()
