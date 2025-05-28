from __future__ import unicode_literals

AUTHOR = 'Алексей Клементьев'
SITENAME = 'WEBfolio'
SITEURL = 'https://LyoshaGodX.github.io/WEBfolio'

TAGS = ['1 семестр', '2 семестр', '3 семестр', '4 семестр', '5 семестр', '6 семестр', '7 семестр', '8 семестр']

SKILLS_TAGS = ['3D', 'Data science', 'Exel', 'Pascal', 'Web разработка', 'git', 'Алгебра', 'Алгоритмы', 'Базы данных', 'Безопасность жизнедеятельности', 'Визуализация данных', 'Гуманитарные науки', 'Иностранный язык', 'История', 'Компьютерная архитектура', 'Копирайт', 'Курсовая работа', 'Математический анализ', 'Матричные вычисления', 'Машинное обучение', 'Менеджмент', 'Практика', 'Программирование', 'Работа с текстом', 'Серверные технологии', 'Символьные вычисления', 'Софт', 'Спорт', 'Таскменеджмент', 'Физика', 'Четкая логика']

PLUGIN_PATHS = ['.']
PLUGINS = ['custom_filters']

THEME = "theme/mytheme"

PATH = 'content'

STATIC_PATHS = ['img']

PAGE_PATHS = ['pages']
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'


TAG_SAVE_AS = '{slug}.html'
TAG_URL = '{slug}.html'

TIMEZONE = 'Europe/Moscow'

GITHUB_URL = 'https://github.com/LyoshaGodX/WEBfolio'

DEFAULT_LANG = 'ru'
SUMMARY_MAX_LENGTH = 10

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

SOCIAL = (('Telegram', 'https://t.me/LyoshaGodX'),)

DEFAULT_PAGINATION = None

# CSS file configuration for the new modern theme
CSS_FILE = 'modern.css'

# Additional configuration for the modern theme
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False