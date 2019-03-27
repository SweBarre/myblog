#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jonas Forsberg'
SITENAME = 'rre.nu'
SITEURL = 'http://localhost:8000'

PATH = 'content'

TIMEZONE = 'Europe/Stockholm'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
        ('Tags', SITEURL+'/tags.html'),
         )

# Social widget
SOCIAL = (
            ('GitHub', 'https://github.com/SweBarre'),
            ('Twitter', 'https://twitter.com/BarreGargamel'),
         )
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
THEME = 'themes/pelican-svbhack'
RELATIVE_URLS = False
USER_LOGO_URL= SITEURL + "/images/barre.png"
ROUND_USER_LOGO = False
#DISQUS_SITENAME=
TAGLINE="your almond in the cyber porridge"

