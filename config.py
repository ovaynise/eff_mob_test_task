from datetime import datetime

MIN_AUTHOR_LENGTH = 2
MIN_AUTHOR_WORDS_ON_NAME = 1
MAX_AUTHOR_WORDS_ON_NAME = 3
MIN_YEAR = 100
MAX_YEAR = datetime.now().year
AUTHOR_REGEX_NAME = r"^[^\d\s][A-Za-zА-Яа-яёЁ\s]+$"
DATABASE_PATCH = 'database.json'
DEFAULT_ID_ON_DB = 12
MIN_TITLE_LENGTH = 4
MIN_BOOK_SEARCH_LENGHT = 2
