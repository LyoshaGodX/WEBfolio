#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Кастомные фильтры для Jinja2 в Pelican
"""

import re
from unidecode import unidecode

def transliterate_slug(text):
    """
    Транслитерирует русский текст в латиницу для создания slug'ов.
    """
    # Используем unidecode для транслитерации
    transliterated = unidecode(text)
    
    # Приводим к нижнему регистру и заменяем все не-буквы/цифры на дефисы
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', transliterated.lower())
    
    # Убираем дефисы в начале и конце
    slug = slug.strip('-')
    
    return slug

def add_custom_filters(pelican):
    """
    Добавляет кастомные фильтры в Jinja2.
    """
    pelican.env.filters['transliterate_slug'] = transliterate_slug

def register():
    """
    Регистрирует плагин в Pelican.
    """
    from pelican import signals
    signals.generator_init.connect(add_custom_filters)
