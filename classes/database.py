import os
import sqlite3

from utils import get_list_from_file
from config import logger, lock, database, quests_config
from classes.quests import Quests


class Database:

    @staticmethod
    def create_database():
        """
        Создание базы данных c номерами профилей
        :return: None
        """
        ads_nums = get_list_from_file("ads_nums.txt")

        if not ads_nums:
            logger.error("Не найдены номера адс профилей")
            return

        if os.path.exists(database):
            os.remove(database)

        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS linea (
                    num_profile INTEGER PRIMARY KEY,
                    lxp INTEGER
                )
            """)
            conn.commit()

            ads_nums = [(int(num),) for num in ads_nums]
            cursor.executemany('INSERT INTO linea (num_profile) VALUES (?)', ads_nums)
            conn.commit()

    @staticmethod
    def print_database():
        """
        Вывод базы данных
        :return:
        """
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            # напечатать названия столбцов
            cursor.execute("PRAGMA table_info(linea)")
            table_info = [col_name[1] for col_name in cursor.fetchall()]

            cursor.execute("SELECT * FROM linea")
            statuses = cursor.fetchall()

            for row in statuses:
                for col_name, value in zip(table_info, row):
                    print(f"{col_name}: {value}", end=" | ")
                print()

    @staticmethod
    def get_columns() -> list[str]:
        """
        Получение столбцов из базы данных
        :return:
        """
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(linea)")
            return [col_name[1] for col_name in cursor.fetchall()]

    @staticmethod
    def _generate_query() -> str:
        """Generate an SQL query to find rows with at least one NULL value."""
        conditions = " OR ".join([f"{quest_name} IS NULL" for quest_name, status in quests_config.items() if status])
        query = f"SELECT * FROM linea WHERE {conditions}"
        return query

    @staticmethod
    def add_col_to_db(column_name: str) -> None:
        """
        Добавление столбца в базу данных
        :param column_name:
        :return:
        """
        # Проверка наличия столбца в таблице
        columns = Database.get_columns()
        database = os.path.join("data", "database.db")

        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()

            if column_name not in columns:
                query_add = f"""
                        ALTER TABLE linea
                        ADD COLUMN {column_name} TEXT
                    """
                cursor.execute(query_add)
                conn.commit()

    @staticmethod
    def update_database() -> None:
        """
        Обновление базы данных, добавление столбцов для квестов
        :return: None
        """
        for quest in Quests:
            Database.add_col_to_db(quest.name)

    @staticmethod
    def change_status(column_name: str, status: str, num_profile: int) -> None:
        """
        Изменение статуса в базе данных
        :param column_name:
        :param status:
        :param num_profile:
        :return:
        """
        Database.add_col_to_db(column_name)

        with lock:
            with sqlite3.connect(database) as conn:
                cursor = conn.cursor()

                query = f"""
                SELECT num_profile
                FROM linea
                WHERE num_profile = :num_profile
                """
                cursor.execute(query, {"num_profile": num_profile})
                if cursor.fetchone():
                    query = f"""
                        UPDATE linea 
                        SET {column_name} = :status
                        WHERE num_profile = :num_profile
                    """
                    cursor.execute(query, {"status": status, "num_profile": num_profile})
                else:
                    query = f"""
                        INSERT INTO linea (num_profile, {column_name})
                        VALUES (:num_profile, :status)
                        """
                    cursor.execute(query, {"status": status, "num_profile": num_profile})

                conn.commit()

    @staticmethod
    def get_profiles() -> list[int]:
        """
        Получение списка профилей у которых среди включенных квестов есть незавершенные
        :return: список номеров профилей
        """
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            query = Database._generate_query()
            cursor.execute(query)
            return [profile[0] for profile in cursor.fetchall()]

    @staticmethod
    def check_status(quest_name: str, profile_num: int) -> bool:
        """
        Проверка статуса квеста
        :param profile_num:
        :param quest_name:
        :return:
        """
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {quest_name} FROM linea WHERE num_profile = :num_profile", {"num_profile": profile_num})
            return cursor.fetchone()[0] in ["done", "not claim"]

    @staticmethod
    def reset_quest_status(quest_number: str) -> None:
        """
        Сброс статуса квеста
        :param quest_name: номер квеста
        :return: None
        """
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE linea SET quest_{quest_number} = NULL")
            conn.commit()
