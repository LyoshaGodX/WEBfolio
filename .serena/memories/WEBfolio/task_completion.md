Что делать при завершении задачи (чеклист):

1. Запустить обновление тегов (если релевантно):
```
python update_skills_tags.py
```
2. Сборка и проверка локально:
```
python -m pelican content
# или
make html
```
3. Просмотреть сайт локально (опционально):
```
python -m pelican --listen
# или
make serve
```
4. Запуск форматирования/линтинга (если настроено):
```
black .
flake8 .
```
5. Закоммитить и запушить изменения в репозиторий:
```
git add -A
git commit -m "Описание выполненной задачи"
git push
```
6. (Опционально) Выполнить публикацию в GitHub Pages:
```
make github
```

Если чего-то в этом списке нет в проекте — обновите `WEBfolio/suggested_commands.md` и `WEBfolio/overview.md` соответственно.