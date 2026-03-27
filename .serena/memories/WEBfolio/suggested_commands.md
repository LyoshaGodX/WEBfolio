Рекомендуемые команды для разработки и деплоя (Windows):

Установка зависимостей:
```
python -m pip install -r requirements.txt
```

Обновление тегов навыков:
```
python update_skills_tags.py
# или через Makefile
make update-tags
```

Сборка сайта (локально):
```
python -m pelican content
# или
make html
```

Запуск локального сервера (просмотр):
```
python -m pelican --listen
# или через Makefile
make serve
# или режим разработки (пересборка при изменениях)
make devserver
```

Публикация на GitHub Pages (если используется):
```
make github
```

Полезные команды Git:
```
git add -A
git commit -m "описание изменений"
git push origin main
```

Примечания для Windows:
- На Windows `make` может отсутствовать; используйте прямые команды Python или `invoke` (`tasks.py`) если настроено.
- Для удобства можно установить `Invoke` (в `requirements.txt`) и запускать задачи через `invoke <task>`.

Локальные инструменты разработки (предложение):
- Форматирование: `black .`
- Линтинг: `flake8 .` (если добавить конфигурацию)
- Установка dev-зависимостей в отдельное окружение (venv) рекомендуется.