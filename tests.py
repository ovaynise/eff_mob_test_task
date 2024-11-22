import unittest
from unittest.mock import patch

from config import MIN_AUTHOR_LENGTH, MIN_TITLE_LENGTH
from library import BookStatus, Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Подготовка данных перед тестами."""
        self.library = Library()
        self.library.books = []

    def test_add_book_success(self):
        """Тест успешного добавления книги."""
        self.library.add_book('Мастер и Маргарита',
                              'Михаил Афанасьевич Булгаков',
                              1967)
        self.assertEqual(len(self.library.books), 1)
        book = self.library.books[0]
        self.assertEqual(book['title'], 'Мастер и Маргарита')
        self.assertEqual(book['author'], 'Михаил Афанасьевич Булгаков')
        self.assertEqual(book['year'], 1967)
        self.assertEqual(book['status'], BookStatus.AVAILABLE.value)

    def test_add_book_invalid_title(self):
        """Тест добавления книги с некорректным названием."""
        with patch('builtins.print') as mocked_print:
            self.library.add_book('A' * (MIN_TITLE_LENGTH - 1),
                                  'Михаил Афанасьевич Булгаков',
                                  1967)
            mocked_print.assert_called_with(
                f'❌ Ошибка: Название книги должно быть больше '
                f'{MIN_TITLE_LENGTH} символов.')
        self.assertEqual(len(self.library.books), 0)

    def test_add_book_invalid_author(self):
        """Тест добавления книги с некорректным автором."""
        with patch('builtins.print') as mocked_print:
            self.library.add_book('Мастер и Маргарита',
                                  'A' * (MIN_AUTHOR_LENGTH - 1),
                                  1967)
            mocked_print.assert_called_with(
                f'❌ Ошибка: Имя автора должно быть больше '
                f'{MIN_AUTHOR_LENGTH} символов.')
        self.assertEqual(len(self.library.books), 0)

    def test_delete_book_success(self):
        """Тест успешного удаления книги."""
        self.library.add_book('Мастер и Маргарита',
                              'Михаил Афанасьевич Булгаков',
                              1967)
        book_id = self.library.books[0]['id']
        self.library.delete_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_delete_book_not_found(self):
        """Тест удаления несуществующей книги."""
        with patch('builtins.print') as mocked_print:
            self.library.delete_book(999)
            mocked_print.assert_called_with(
                '❌ Ошибка: Книга с ID 999 не найдена.')

    def test_search_books_found(self):
        """Тест успешного поиска книг."""
        self.library.add_book(
            'Мастер и Маргарита',
            'Михаил Афанасьевич Булгаков',
            1967)
        self.library.add_book(
            'Братья Карамазовы',
            'Федор Достоевский',
            1866)
        with patch('builtins.print') as mocked_print:
            self.library.search_books('Мастер')
            mocked_print.assert_any_call(
                {'id': 1,
                 'title': 'Мастер и Маргарита',
                 'author': 'Михаил Афанасьевич Булгаков',
                 'year': 1967, 'status': 'в наличии'})
            mocked_print.assert_any_call('✅ Найдено 1 книг(а).')

    def test_list_books(self):
        """Тест отображения всех книг."""
        self.library.add_book(
            'Мастер и Маргарита',
            'Михаил Афанасьевич Булгаков',
            1967)
        self.library.add_book(
            'Братья Карамазовы',
            'Федор Достоевский',
            1866)
        with patch('builtins.print') as mocked_print:
            self.library.list_books()
            mocked_print.assert_any_call(
                {'id': 1, 'title': 'Мастер и Маргарита',
                 'author': 'Михаил Афанасьевич Булгаков',
                 'year': 1967, 'status': 'в наличии'})
            mocked_print.assert_any_call(
                {'id': 2,
                 'title': 'Братья Карамазовы',
                 'author': 'Федор Достоевский',
                 'year': 1866, 'status': 'в наличии'})
            mocked_print.assert_any_call('✅ Всего книг в библиотеке: 2.')

    def test_update_book_status_success(self):
        """Тест успешного изменения статуса книги."""
        self.library.add_book(
            'Мастер и Маргарита',
            'Михаил Афанасьевич Булгаков',
            1967)
        book_id = self.library.books[0]['id']
        with (patch('builtins.input', side_effect=['2']),
              patch('builtins.print') as mocked_print):
            self.library.update_book_status(book_id)
            self.assertEqual(self.library.books[0]['status'],
                             BookStatus.ISSUED.value)
            mocked_print.assert_any_call(
                "✅ Статус книги с ID 1 обновлен на 'выдана'.")


if __name__ == '__main__':
    unittest.main()
