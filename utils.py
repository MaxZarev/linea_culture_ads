import os.path
import random
import time


def sleep_random(min: float=1, max: float=3) -> None:
    time.sleep(random.uniform(min, max))


def get_list_from_file(path: str) -> list[str]:
    """
    Читает файл и возвращает список строк
    :param path: название файла
    :return:
    """
    with open(os.path.join("data", path), "r") as file:
        return file.read().splitlines()