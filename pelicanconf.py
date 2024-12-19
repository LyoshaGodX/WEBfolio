from __future__ import unicode_literals

AUTHOR = 'Алексей Клементьев'
SITENAME = 'WEBfolio'
SITEURL = 'https://LyoshaGodX.github.io/WEBfolio'

TAGS = ['1 семестр', '2 семестр', '3 семестр', '4 семестр', '5 семестр', '6 семестр', '7 семестр', '8 семестр']

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