#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для автоматического обновления списка тегов навыков в pelicanconf.py
"""

import os
import re

# Путь к каталогу с файлами дисциплин
DISCIPLINES_DIR = 'content/posts'
CONFIG_FILE = 'pelicanconf.py'

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

def update_pelicanconf():
    """Обновляет список SKILLS_TAGS в pelicanconf.py"""
    if not os.path.exists(CONFIG_FILE):
        print(f"Файл конфигурации {CONFIG_FILE} не найден!")
        return False
    
    skills_tags = parse_all_tags()
    
    if not skills_tags:
        print("Теги навыков не найдены.")
        return False
    
    # Читаем содержимое файла
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Создаем новую строку SKILLS_TAGS
    new_skills_line = f"SKILLS_TAGS = {skills_tags}"
    
    # Ищем существующую строку SKILLS_TAGS и заменяем её
    pattern = r'^SKILLS_TAGS\s*=.*$'
    if re.search(pattern, content, re.MULTILINE):
        updated_content = re.sub(pattern, new_skills_line, content, flags=re.MULTILINE)
        print("Обновлен существующий список SKILLS_TAGS")
    else:
        # Если строки нет, добавляем после TAGS
        tags_pattern = r'(^TAGS\s*=.*$)'
        if re.search(tags_pattern, content, re.MULTILINE):
            updated_content = re.sub(
                tags_pattern, 
                r'\1\n\n' + new_skills_line, 
                content, 
                flags=re.MULTILINE
            )
            print("Добавлен новый список SKILLS_TAGS")
        else:
            print("Не найдена переменная TAGS в файле конфигурации")
            return False
    
    # Записываем обновленное содержимое
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Файл {CONFIG_FILE} успешно обновлен!")
    print(f"Обновлено {len(skills_tags)} тегов навыков:")
    for i, tag in enumerate(skills_tags, 1):
        print(f"  {i:2d}. {tag}")
    
    return True

def main():
    """Основная функция."""
    print("Автоматическое обновление списка тегов навыков...")
    print("-" * 60)
    
    if update_pelicanconf():
        print("\n" + "=" * 60)
        print("✅ ЗАДАЧА ВЫПОЛНЕНА УСПЕШНО!")
        print("Теперь можно пересобрать сайт командой: python -m pelican content")
    else:
        print("\n" + "=" * 60)
        print("❌ ОШИБКА: Не удалось обновить конфигурацию")

if __name__ == "__main__":
    main()
