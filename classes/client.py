from __future__ import annotations

import random

import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from classes.database import Database
from utils import sleep_random
from config import logger, quests_config
from classes.quests import Quests


class Client:
    def __init__(self, ads_num: int):
        self.ads_num = ads_num
        self.driver = self._profile_start()
        self._tab_prepare()

    def _profile_start(self) -> WebDriver:
        """
        Запуск профиля
        :return: объект драйвера
        """
        if not (response := self._check_browser()):
            url = f'http://local.adspower.com:50325/api/v1/browser/start'
            params = {'serial_number': self.ads_num}
            response = requests.get(url, params=params)
            response.raise_for_status()
            response = response.json()
            if response["code"] != 0:
                raise ValueError(f"Please check ads_id {response['msg']}")

        chrome_driver = response["data"]["webdriver"]
        service = Service(executable_path=chrome_driver)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", response["data"]["ws"]["selenium"])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def _check_browser(self) -> dict | bool:
        try:
            url = f"http://local.adspower.com:50325/api/v1/browser/active"
            params = {'serial_number': self.ads_num}

            response = requests.get(url, params=params)
            response.raise_for_status()
            response = response.json()
            if response.get("data", {}).get("status") == "Active":
                return response
            else:
                return False
        except requests.RequestException as e:
            print(f"Error checking Ads browser: {e}")
            return False

    def _tab_prepare(self) -> None:
        """
        Закрывает вкладки кроме одной и разворачивает окно на весь экран
        :return:
        """

        sleep_random(4, 6)

        tabs = self._filtering_tab()

        if len(tabs) > 1:
            for tab in tabs[1:]:
                try:
                    self.driver.switch_to.window(tab)
                    self.driver.close()
                except Exception as ex:
                    logger.error(f"{self.ads_num} _tab_prepare error: {ex}")

        self.driver.switch_to.window(tabs[0])
        self.driver.maximize_window()

    def _filtering_tab(self) -> list[str]:
        """
        Подготовка вкладок с игнором вкладки Rabby Offscreen Page
        :return: список вкладок
        """
        draft_tabs = self.driver.window_handles
        tabs = []

        if len(draft_tabs) > 1:
            for tab in draft_tabs:
                self.driver.switch_to.window(tab)
                if not self.driver.title == "Rabby Offscreen Page":
                    tabs.append(tab)
            return tabs
        return draft_tabs

    def open_url(self, url: str) -> None:
        """
        Открытие страницы по url
        :param url: адрес страницы
        :return: None
        """
        self.driver.get(url)

    def profile_close(self) -> None:
        """
        Закрытие профиля
        :return:
        """
        try:
            self.driver.quit()
            sleep_random(4, 6)
            for _ in range(5):
                if self._check_status():
                    url = "http://local.adspower.com:50325/api/v1/browser/stop"
                    params = {"serial_number": self.ads_num}
                    requests.get(url, params=params)
                    sleep_random(4, 6)
                else:
                    return
        except Exception as ex:
            logger.error(f"{self.ads_num} profile_close error: {ex}")

    def _check_status(self):
        """
        Проверка статуса браузера
        :return:
        """
        url = f"http://local.adspower.com:50325/api/v1/browser/active"
        params = {"serial_number": self.ads_num}
        response = requests.get(url, params=params)
        if response.json()["data"]["status"] == "Active":
            return True
        return False

    def check_element(self, xpath: str, timeout: int = 15) -> WebElement | None:
        """
        Проверка наличия элемента на странице
        :param xpath:
        :param timeout:
        :return:
        """
        for _ in range(timeout):
            try:
                return self.driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                sleep_random(0.5, 1.5)
        return None

    def get_text(self, xpath: str, timeout: int = 15) -> str:
        """
        Получение текста элемента
        :param xpath:
        :param timeout:
        :return:
        """
        if element := self.check_element(xpath, timeout):
            return element.text
        return ""

    def click(self, xpath: str, timeout: int = 15, raiser: bool = True):
        """
        Нажатие на элемент
        :param xpath:
        :param timeout:
        :param raiser:
        :return:
        """
        sleep_random(0.2, 0.4)
        try:
            if element := self.check_element(xpath, timeout):
                element.click()
                sleep_random(0.5, 1.5)
                return True
            else:
                if raiser:
                    logger.warning(f"{self.ads_num} click: Element by xpath {xpath} not found")
        except Exception:
            if raiser:
                logger.error(f"{self.ads_num} click: Element by xpath {xpath} not found")


class Linea(Client):
    linea_url = "https://app.layer3.xyz/campaigns/linea-culture-szn"

    def __init__(self, ads_num: int):
        super().__init__(ads_num)

    def run_quests(self):
        """
        Запуск квестов
        :return:
        """
        for _ in range(random.randint(2, 4)):
            self.open_linea()
            self.click("//p[text()='Later']/parent::button", 5, raiser=False)
            self.get_lxp()

            result = [self.run_quest(quest) for quest in Quests if quests_config.get(quest.name)]
            if all(result):
                break

    def run_quest(self, quest: Quests) -> bool:
        """
        Запуск конкретного квеста
        :param quest:
        :return:
        """
        if self.check_element(f"//a[contains(@href, '{quest.value.name}')]//span[text()='Completed']", 5):
            Database.change_status(quest.name, "done", self.ads_num)
            return True

        if Database.check_status(quest.name, self.ads_num):
            return True

        logger.info(f"{self.ads_num} Running quest: {quest.value.name}")
        self.open_url(quest.value.layer_url)

        sleep_random(3, 5)

        # проверяем на странице конкретного квеста, что квест уже выполнен
        if self.check_element("//h2[text()='Finish all steps']/following-sibling::div//span[text()='Completed']", 5):
            Database.change_status(quest.name, "done", self.ads_num)
            return True

        # нажимаем на кнопку "Continue" нужное количество раз
        for _ in range(quest.value.continue_count):
            self.click("//button[text()='Continue']")
            sleep_random(1, 5)

        # отвечаем на квиз, если он есть
        if quest.value.quiz_answer:
            self.click(f"//button[contains(text(), {quest.value.quiz_answer})]")
            self.click("//button[text()='Continue']")
            sleep_random(3, 5)

        # нажимаем на кнопку "Verify" нужное количество раз
        if quest.value.verify_count:
            for _ in range(quest.value.verify_count):
                self.click("//button[text()='Verify']")
                sleep_random(10, 15)
                if self.check_element("//p[text()='No matching transactions found']", ):
                    Database.change_status(quest.name, "not claim", self.ads_num)
                    return True

        if vote_options := quest.value.vote_options:
            self.click("//button[text()='Continue']")
            vote = random.randint(1, vote_options)
            self.click(f"//button[@role='radio'][{vote_options}]")
            sleep_random(3, 5)
            self.click("//button[text()='Continue']")
            sleep_random(10, 15)
            logger.info(f"{self.ads_num} Не забудь сминтить кубы")
            Database.change_status(quest.name, "done", self.ads_num)
            return True


        # пропускаем страницу заданием, если это нужно
        if quest.value.skip:
            self.click("//button[text()='Skip']")
            sleep_random(3, 5)

        return False  # возвращаем False, чтобы была еще одна проверка всех квестов

    def open_linea(self):
        if not self.driver.current_url == self.linea_url:
            # делаем несколько попыток открыть страницу с ожиданием прохождения клаудфлейр
            self.open_url(self.linea_url)
            for _ in range(5):
                if self.check_element("//h1[text()='Linea Culture SZN']"):
                    return
                sleep_random(20, 30)
                self.driver.refresh()

    def get_lxp(self):
        sleep_random(3, 5)
        lxp = self.get_text("//div[text()='Total L•XP']/following-sibling::div")
        logger.info(f"{self.ads_num} LXP: {lxp}")
        Database.change_status("lxp", str(lxp), self.ads_num)

