#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга всех тегов из файлов дисциплин и генерации списка навыков
"""

import os
import re

# Путь к каталогу с файлами дисциплин
DISCIPLINES_DIR = 'content/posts'

def parse_all_tags():
    """Собирает все уникальные теги из файлов дисциплин, кроме тегов-семестров."""
    semester_tags = {f"{i} семестр" for i in range(1, 9)}
    tags_set = set()
    
    if not os.path.exists(DISCIPLINES_DIR):
        print(f"Директория {DISCIPLINES_DIR} не найдена!")
        return []
        
    for fname in os.listdir(DISCIPLINES_DIR):
        if fname.endswith('.md'):
            file_path = os.path.join(DISCIPLINES_DIR, fname)
            try:
                with open(file_path, encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith('tags:'):
                            tags_line = line.split(':', 1)[1].strip()
                            tags = [t.strip() for t in tags_line.split(',')]
                            tags_set.update(tags)
                            break
            except Exception as e:
                print(f"Ошибка при чтении файла {fname}: {e}")
                
    # Исключаем семестровые теги и пустые строки
    skills_tags = [t for t in tags_set if t and t not in semester_tags]
    return sorted(skills_tags)

def main():
    """Основная функция для демонстрации работы парсера."""
    print("Парсинг тегов из файлов дисциплин...")
    print("-" * 50)
    print(f"Проверяем директорию: {DISCIPLINES_DIR}")
    print(f"Директория существует: {os.path.exists(DISCIPLINES_DIR)}")
    
    skills_tags = parse_all_tags()
    
    if skills_tags:
        print(f"Найдено {len(skills_tags)} тегов навыков:")
        for i, tag in enumerate(skills_tags, 1):
            print(f"{i:2d}. {tag}")
        
        print("\n" + "-" * 50)
        print("Список тегов для добавления в pelicanconf.py:")
        print(f"SKILLS_TAGS = {skills_tags}")
        
        print("\n" + "-" * 50)
        print("HTML код для шаблона:")
        html_links = []
        for tag in skills_tags:
            # Создаем slug для тега (заменяем пробелы и спецсимволы на дефисы)
            slug = re.sub(r'[^a-zA-Zа-яА-Я0-9]+', '-', tag.lower()).strip('-')
            html_links.append(f'<a href="{{{{ SITEURL }}}}/{slug}.html">{tag}</a>')
        
        html_code = ' | '.join(html_links)
        print(f"<p>{html_code}</p>")
        
    else:
        print("Теги навыков не найдены.")

if __name__ == "__main__":
    main()
