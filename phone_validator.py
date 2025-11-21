import re
import requests
from typing import List

class PhoneNumberValidator:
    """Класс для проверки номеров телефонов"""
    def __init__(self):
        # Здесь будет регулярное выражение
        # Номера в форматах: +7XXXxxxXXxx, 8XXXxxxXXxx
        # X - цифры, между ними могут быть пробелы, дефисы
        # Скобки могут быть только вокруг кода оператора (3 цифры после +7/8)
        self.phone_pattern = re.compile(
            r'(?:\+7|8)[\s\-]?(?:\s?\(\d{3}\)\s?|\s?\d{3}\s?|\s?\(\d{3}\)|\d{3})[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
        )

    def validate_phone(self, phone: str) -> bool:
        """Проверка корректности для одного номера телефона"""
        if not phone:
            return False

        if not self.phone_pattern.search(phone):
            return False

        cleaned = re.sub(r'[^\d+]', '', phone)

        # Проверка длины:
        # +79123456789 - 12 символов
        # 89123456789 - 11 символов
        if cleaned.startswith('+7') and len(cleaned) == 12:
            return True
        elif cleaned.startswith('8') and len(cleaned) == 11:
            return True
        else:
            return False

    def find_phones_in_text(self, text: str) -> List[str]:
        """Ищет номера телефонов в тексте"""
        if not text:
            return []

        # Находим все
        possible_phones = self.phone_pattern.findall(text)
        # Просто убираем пробелы, регулярка уже отфильтровало некорректные
        return [phone.strip() for phone in possible_phones]

    def find_phones_in_file(self, file_path: str) -> List[str]:
        """Поиск номера телефона в файле"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                return self.find_phones_in_text(text)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден")
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}")
            return []

    def find_phones_on_website(self, url: str) -> List[str]:
        """Поиск номера телефона на сайте"""
        try:
            response = requests.get(url, timeout=10)
            return self.find_phones_in_text(response.text)
        except Exception as e:
            print("Ошибка при загрузке страницы")
            return []

def main():
    """Интерфейс для пользователя"""

    validator = PhoneNumberValidator()

    print("Поиск российских номеров телефонов")
    print("Выберете действие")
    print("1. Проверить один номер")
    print("2. Найти номера в тексте")
    print("3. Найти номера в файле")
    print("4. Найти номера на сайте")

    choice = input("Ваш выбор: 1 - 4: ")

    if choice == '1':
        phone = input("Введите номер телефона: ")
        if validator.validate_phone(phone):
            print("Это корректный номер!")
        else:
            print("Это некорректный номер!")
    elif choice == '2':
        text = input("Введите текст: ")
        phones = validator.find_phones_in_text(text)
        if phones:
            print(f"Найдено номеров: {len(phones)}")
            for i, phone in enumerate(phones, 1):
                print(f"{i}. {phone}")
        else:
            print("Номера не найдены")

    elif choice == '3':
        file_path = input("Введите путь к файлу: ")
        phones = validator.find_phones_in_file(file_path)
        if phones:
            print(f"Найдено номеров: {len(phones)}")
            for i, phone in enumerate(phones, 1):
                print(f"{i}. {phone}")
        else:
            print("Номера не найдены")

    elif choice == '4':
        url = input("Введите URL сайта: ")
        phones = validator.find_phones_on_website(url)
        if phones:
            print(f"Найдено номеров: {len(phones)}")
            for i, phone in enumerate(phones, 1):
                print(f"{i}. {phone}")
        else:
            print("Номера не найдены")

    else:
        print("Неверный выбор!")

if __name__ == "__main__":
    main()
