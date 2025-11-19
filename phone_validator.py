import re
import requests
from typing import List, Tuple

class PhoneNumberValidator:
    """Класс для проверки номеров телефонов"""
    def __init__(self):
        # Здесь будет регулярное выражение
        # Номера в форматах: +7XXXxxxXXxx, 8XXXxxxXXxx
        # X - цифры, между ними могут быть пробелы, дефисы
        # Скобки могут быть только вокруг кода оператора (3 цифры после +7/8)
        self.phone_pattern = re.compile(
            r''
        )
    def validate_phone(self, phone: str) -> bool:
        """Проверка корректности для одного номера телефона"""
        pass

    def find_phone_in_text(self, text: str) -> List[str]:
        """Ищет номера телефонов в тексте"""
        pass
    def find_phone_in_file(self, text: str) -> List[str]:
        """Поиск номера телефона в файле"""
        pass
    def find_phone_on_website(self, text: str) -> List[str]:
        """Поиск номера телефона на сайте"""
def main():
    """Интерфейс для пользователя"""
    pass

