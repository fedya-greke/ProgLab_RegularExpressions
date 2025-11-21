import unittest
import os
from phone_validator import PhoneNumberValidator

class TestPhoneNumberValidator(unittest.TestCase):
    """Unit-тесты для класса PhoneNumberValidator"""

    def setUp(self):
        """Подготовка тестового окружения перед каждым тестом"""
        self.validator = PhoneNumberValidator()

    def test_validate_phone_correct_numbers(self):
        """Тест корректности номеров"""
        correct_numbers = [
            "+7-912-345-67-89",
            "8 (912) 345-67-89",
            "+7(912)3456789",
            "89123456789",
            "8-912-345-67-89",
            "+7 (912) 345 67 89",
            "8(912)345-67-89"
        ]

        for phone in correct_numbers:
            # Запускает несколько похожих тестов.
            # Если один упадёт - увидим какой именно.
            with self.subTest(phone=phone):
                self.assertTrue(
                    self.validator.validate_phone(phone),
                    f"Номер {phone} должен быть корректным"
                )

    def test_validate_phone_incorrect_numbers(self):
        """Тест некорректных номеров"""
        incorrect_numbers = [
            "79123456789",  # начинается с 7 без +
            "123-456-789",  # мало цифр
            "+7-abc-def-gh-ij",  # есть буквы
            "8912345678",  # 10 цифр вместо 11
            "891234567890",  # 12 цифр вместо 11
            "8 (912 345(56) 78",  # неправильные скобки
            "8(9123)456789",  # 4 цифры в скобках
            "8(91)23456789",  # 2 цифры в скобках
            "",  # пустая строка
            "телефон",  # текст вместо номера
            "+7-912-345-67-8",  # неполный номер
        ]

        for phone in incorrect_numbers:
            with self.subTest(phone=phone):
                self.assertFalse(
                    self.validator.validate_phone(phone),
                    f"Номер {phone} должен быть некорректным"
                )

    def test_find_phones_in_text_single_phone(self):
        """Тест поиска одного номера в тексте"""
        text = "Мой номер телефона: +7-912-345-67-89"
        expected = ["+7-912-345-67-89"]
        result = self.validator.find_phones_in_text(text)
        self.assertEqual(result, expected)

    def test_find_phones_in_text_multiple_phones(self):
        """Тест поиска нескольких номеров в тексте"""
        text = """
                Контакты: 
                мобильный +7-912-345-67-89, 
                рабочий 8 495 123 45 67,
                бесплатный 8800-555 35 35
                """
        expected = ["+7-912-345-67-89", "8 495 123 45 67", "8800-555 35 35"]
        result = self.validator.find_phones_in_text(text)
        self.assertEqual(result, expected)

    def test_find_phones_in_text_no_phone(self):
        """Тест поиска телефонов в тексте, но их нет"""
        text = """Это текст без телефонных номеров"""
        result = self.validator.find_phones_in_text(text)
        self.assertEqual(result, [])

    def test_find_phones_in_text_mixed_content(self):
        """Тест поиска в тексте с правильными и неправильными номерами"""
        text = """
        Правильные: +7-912-345-67-89 и 8-800-555-35-35
        Неправильные: 79123456789 и 123-456-789
        """
        expected = ["+7-912-345-67-89", "8-800-555-35-35"]
        result = self.validator.find_phones_in_text(text)
        self.assertEqual(result, expected)

    def test_find_phones_in_file_exists(self):
        """Тест поиска номеров в существующем файле"""
        # Создаём временный файл для теста
        test_content = """
        Контакты компании:
        Отдел продаж: +7-495-123-45-67
        Техподдержка: 8-800-555-35-35
        """

        test_file = "test_phones.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)

        try:
            expected = ["+7-495-123-45-67", "8-800-555-35-35"]
            result = self.validator.find_phones_in_file(test_file)
            self.assertEqual(result, expected)
        finally:
            # Удаляем временный файл после теста
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_find_phones_in_empty_file(self):
        """Тест поиска в пустом файле"""
        test_file = "empty_test.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("")

        try:
            result = self.validator.find_phones_in_file(test_file)
            self.assertEqual(result, [])
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_find_phones_in_file_not_exists(self):
        """Тест поиска в несуществующем файле"""
        result = self.validator.find_phones_in_file("nonexistent_file.txt")
        self.assertEqual(result, [])

    def test_empty_string_validation(self):
        """Тест валидации пустой строки"""
        self.assertFalse(self.validator.validate_phone(""))

    def test_find_phones_on_website(self):
        """Тест поиска на веб-странице"""
        try:
            # Простая тестовая страница
            result = self.validator.find_phones_on_website("https://httpbin.org/html")
            self.assertIsInstance(result, list)
        # Пропускается если нет интернета
        except Exception:
            self.skipTest("Нет интернет-соединения")

if __name__ == "__main__":
    unittest.main()
