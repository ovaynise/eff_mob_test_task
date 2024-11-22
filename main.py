import json
import re
from enum import Enum
from typing import Dict, List, Optional

from config import (AUTHOR_REGEX_NAME, DATABASE_PATCH, DEFAULT_ID_ON_DB,
                    MAX_AUTHOR_WORDS_ON_NAME, MIN_AUTHOR_LENGTH,
                    MIN_AUTHOR_WORDS_ON_NAME, MIN_BOOK_SEARCH_LENGHT,
                    MIN_TITLE_LENGTH, MIN_YEAR, MAX_YEAR)


class BookStatus(Enum):
    """Класс со статусами книг."""
    AVAILABLE = 'в наличии'
    ISSUED = 'выдана'


class Library:
    db = DATABASE_PATCH

    def __init__(self):
        self.books = self.load_database()

    def load_database(self) -> List[Dict]:
        """Функция загружает данные из json."""
        try:
            with open(self.db, 'r', encoding='utf-8') as database:
                return json.load(database)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_database(self) -> None:
        """Функция сохраняет данные в БД в json."""
        with open(self.db, 'w', encoding='utf-8') as database:
            json.dump(self.books, database, indent=4, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int) -> None:
        """Функция добавляет книгу в базу данных и валидирует данные."""
        if not self.validate_title(title):
            return

        if not self.validate_author(author):
            return

        if not self.validate_year(year):
            return

        new_id = max((book.get('id') for book in self.books),
                     default=DEFAULT_ID_ON_DB) + 1
        self.books.append({
            'id': new_id,
            'title': title,
            'author': author,
            'year': year,
            'status': BookStatus.AVAILABLE.value
        })
        self.save_database()
        self.show_message(f'Книга "{title}" добавлена с ID {new_id}.')

    def validate_title(self, title: str) -> bool:
        """Валидатор проверяет название книги."""

        if len(title) < MIN_TITLE_LENGTH:
            self.show_message('Ошибка: Название книги должно '
                              f'быть больше {MIN_TITLE_LENGTH} символов.',
                              success=False)
            return False
        return True

    def validate_author(self, author: str) -> bool:
        """Валидатор проверяет имя автора на соответствие ограничениям."""
        if len(author) < MIN_AUTHOR_LENGTH:
            self.show_message('Ошибка: Имя автора должно '
                              f'быть больше {MIN_AUTHOR_LENGTH} символов.',
                              success=False)
            return False

        words = author.split()
        if (len(words) < MIN_AUTHOR_WORDS_ON_NAME or len(words) >
                MAX_AUTHOR_WORDS_ON_NAME):
            self.show_message(f'Ошибка: Имя автора должно'
                              f' содержать от {MIN_AUTHOR_WORDS_ON_NAME} '
                              f'до {MAX_AUTHOR_WORDS_ON_NAME}'
                              f' слов.', success=False)
            return False

        if not re.match(AUTHOR_REGEX_NAME, author):
            self.show_message('Ошибка: Имя автора не должно'
                              ' содержать цифры и должно начинаться с буквы.',
                              success=False)
            return False

        return True

    def validate_year(self, year: int) -> bool:
        """Валидатор проверяет год издания."""
        if year <= MIN_YEAR:
            self.show_message('Ошибка: Год издания должен'
                              f' быть больше {MIN_YEAR}.', success=False)
            return False
        if year > MAX_YEAR:
            self.show_message('Ошибка: Год издания не может быть'
                              f' больше текущего года ({MAX_YEAR}).',
                              success=False)
            return False
        return True

    def delete_book(self, book_id: int) -> None:
        """Функция удаляет книгу по ID."""
        book_to_delete = next(
            (book for book in self.books if book['id'] == book_id), None)
        if not book_to_delete:
            self.show_message(f'Ошибка: Книга с ID {book_id} '
                              f'не найдена.', success=False)
            return

        self.books.remove(book_to_delete)
        self.save_database()
        self.show_message(f'Книга с ID {book_id} успешно удалена.')

    def search_books(self, keyword: str) -> None:
        """Ищет книги по ключевому слову."""
        if len(keyword) < MIN_BOOK_SEARCH_LENGHT:
            self.show_message('Ошибка: Ключевое слово'
                              f' должно быть больше {MIN_BOOK_SEARCH_LENGHT} '
                              f'символов.',
                              success=False)
            return

        found = [
            book for book in self.books
            if keyword.lower() in str(book['title']).lower()
            or keyword.lower() in str(book['author']).lower()
            or keyword.lower() in str(book['year'])
        ]
        if found:
            for book in found:
                print(book)
            self.show_message(f'Найдено {len(found)} книг(а).')
        else:
            self.show_message('Книг не найдено.', success=False)

    def list_books(self) -> None:
        """Выводит список всех книг."""
        if self.books:
            for book in self.books:
                print(book)
            self.show_message(f'Всего книг в библиотеке: {len(self.books)}.')
        else:
            self.show_message('В библиотеке пока нет книг.',
                              success=False)

    def update_book_status(self, book_id: int) -> None:
        """Изменяет статус книги."""
        book_to_update = next(
            (book for book in self.books if book['id'] == book_id), None)
        if not book_to_update:
            self.show_message(f'Ошибка: Книга с ID {book_id} '
                              f'не найдена.', success=False)
            return

        while True:
            print('\nВыберите новый статус:')
            status_map = {str(index): status.value for index, status in
                          enumerate(BookStatus, start=1)}
            status_map['0'] = 'Вернуться в главное меню'

            for index, status in status_map.items():
                print(f'{index}. {status}')

            choice = input('Введите номер статуса или текст (0 для возврата):')
            if choice == '0':
                print('Возврат в главное меню.')
                return

            if choice in status_map and choice != '0':
                new_status = status_map[choice]
                break
            elif choice in [status.value for status in BookStatus]:
                new_status = choice
                break
            else:
                print('Неверный выбор статуса. Попробуйте снова.')

        book_to_update['status'] = new_status
        self.save_database()
        self.show_message(f"Статус книги с ID {book_id} обновлен на "
                          f"'{new_status}'.")

    @staticmethod
    def show_message(message: str, success: bool = True) -> None:
        """Выводит сообщение об успешном или неуспешном выполнении операции."""
        if success:
            print(f'✅ {message}')
        else:
            print(f'❌ {message}')


class LibraryApp:
    def __init__(self):
        self.library = Library()

    def get_valid_input(self, prompt: str, validation_func,
                        input_type: type = str) -> Optional[str]:
        """Получает валидный ввод от пользователя с проверкой."""
        while True:
            value = input(prompt)
            if value == '0':
                print('Возврат в главное меню.')
                return None
            try:
                value = input_type(value)
                if validation_func(value):
                    return value
            except ValueError:
                self.library.show_message(
                    f'Ошибка: Ожидается {input_type.__name__}.',
                    success=False)

    def main_menu(self) -> None:
        """Главное меню приложения."""
        while True:
            print('\nМеню:')
            print('1. Добавить книгу')
            print('2. Удалить книгу')
            print('3. Искать книгу')
            print('4. Показать все книги')
            print('5. Изменить статус книги')
            print('6. Выйти')

            choice = input('Выберите действие: ')
            if choice == '1':
                self.add_book_menu()
            elif choice == '2':
                self.delete_book_menu()
            elif choice == '3':
                self.search_books_menu()
            elif choice == '4':
                self.library.list_books()
            elif choice == '5':
                self.update_status_menu()
            elif choice == '6':
                print('Выход из программы.')
                break
            else:
                self.library.show_message(
                    'Неверный выбор. Попробуйте снова.',
                    success=False)

    def add_book_menu(self) -> None:
        """Меню добавления книги."""
        print('Введите данные для добавления книги ('
              '0 для возврата в главное меню).')
        title = self.get_valid_input('Название книги: ',
                                     self.library.validate_title, str)
        if title is None:
            return

        author = self.get_valid_input('Автор книги: ',
                                      self.library.validate_author, str)
        if author is None:
            return

        year = self.get_valid_input(
            'Год издания: ', self.library.validate_year, int)
        if year is None:
            return

        self.library.add_book(title, author, year)

    def delete_book_menu(self) -> None:
        """Меню удаления книги."""
        print('Введите ID книги для удаления (0 для возврата в главное меню).')
        book_id = self.get_valid_input(
            'ID книги: ', lambda x: x > 0, int)
        if book_id is None:
            return

        self.library.delete_book(book_id)

    def search_books_menu(self) -> None:
        """Меню поиска книг."""
        print('Введите ключевое слово для поиска (0 для возврата в '
              'главное меню).')
        keyword = self.get_valid_input(
            'Ключевое слово: ', lambda x: len(x) > 1, str)
        if keyword is None:
            return

        self.library.search_books(keyword)

    def update_status_menu(self) -> None:
        """Меню изменения статуса книги."""
        print('Введите ID книги для изменения статуса '
              '(0 для возврата в главное меню).')
        book_id = self.get_valid_input('ID книги: ',
                                       lambda x: x > 0, int)
        if book_id is None:
            return

        self.library.update_book_status(book_id)


if __name__ == '__main__':
    app = LibraryApp()
    app.main_menu()
