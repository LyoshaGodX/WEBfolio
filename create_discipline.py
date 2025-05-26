from flask import Flask, request, render_template_string
import os
import re

app = Flask(__name__)

# Путь к каталогу с файлами дисциплин
DISCIPLINES_DIR = 'content/posts'

def parse_all_tags():
    """Собирает все уникальные теги из файлов дисциплин, кроме тегов-семестров."""
    semester_tags = {f"{i} семестр" for i in range(1, 9)}
    tags_set = set()
    for fname in os.listdir(DISCIPLINES_DIR):
        if fname.endswith('.md'):
            with open(os.path.join(DISCIPLINES_DIR, fname), encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('tags:'):
                        tags_line = line.split(':', 1)[1].strip()
                        tags = [t.strip() for t in tags_line.split(',')]
                        tags_set.update(tags)
                        break
    # Исключаем семестровые теги и пустые строки
    return sorted([t for t in tags_set if t and t not in semester_tags])

def translit(text):
    """Транслитерирует русский текст в латиницу для slug."""
    # Простейшая таблица транслитерации
    ru =   u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    en =  ("a","b","v","g","d","e","e","zh","z","i","y","k","l","m","n","o","p","r","s","t","u","f","h","ts","ch","sh","sch","","y","","e","yu","ya")
    tr = {ord(r):e for r,e in zip(ru, en)}
    tr.update({ord(r.upper()):e.capitalize() for r,e in zip(ru, en)})
    text = text.translate(tr)
    # Заменяем все не-буквы/цифры на "-"
    import re
    text = re.sub(r'[^a-zA-Z0-9]+', '-', text)
    text = text.strip('-').lower()
    return text

def get_used_images():
    """Возвращает множество имен файлов, которые уже используются в featured_image."""
    used = set()
    for fname in os.listdir(DISCIPLINES_DIR):
        if fname.endswith('.md'):
            with open(os.path.join(DISCIPLINES_DIR, fname), encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('featured_image:'):
                        img_path = line.split(':', 1)[1].strip()
                        img_name = os.path.basename(img_path)
                        if img_name:
                            used.add(img_name)
                        break
    return used

def get_unused_images():
    """Возвращает список имен файлов из content/img, которые не используются ни в одном посте."""
    img_dir = os.path.join('content', 'img')
    if not os.path.exists(img_dir):
        return []
    all_imgs = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
    used_imgs = get_used_images()
    unused = [f for f in all_imgs if f not in used_imgs]
    return sorted(unused)

@app.route('/')
def index():
    all_tags = parse_all_tags()
    unused_images = get_unused_images()
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Создание дисциплины</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
    <style>
        body {
            background-color: #f8f9fa;
        }
        .form-container {
            max-width: 800px; /* Максимальная ширина формы */
            margin: 50px auto; /* Отступ сверху и центрирование */
            padding: 20px;
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        #semester-value {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h1 class="mb-4 text-center">Создание новой дисциплины</h1>
        <form id="discipline-form" method="post" action="/create_discipline">
            <div class="mb-3">
                <label for="title" class="form-label">Название дисциплины (или проекта):</label>
                <input type="text" name="title" id="title" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Теги (выберите из существующих или добавьте новые):</label>
                <div id="existing-tags" class="mb-2">
                    {% for tag in all_tags %}
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" name="existing_tags" value="{{ tag }}" id="tag-{{ loop.index }}">
                            <label class="form-check-label" for="tag-{{ loop.index }}">{{ tag }}</label>
                        </div>
                    {% endfor %}
                </div>
                <input type="text" name="tags" id="tags" class="form-control" placeholder="Новые теги через запятую">
            </div>            <div class="mb-3">
                <label for="summary" class="form-label">Краткое описание:</label>
                <input type="text" name="summary" id="summary" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Подробное описание дисциплины:</label>
                <textarea name="description" id="description" class="form-control" rows="5" placeholder="Детальное описание дисциплины, ее целей, задач и особенностей..."></textarea>
                <div class="form-text">Этот блок будет размещен перед списком выполненных работ. Поле необязательное.</div>
            </div>
            <div class="mb-3">
                <label for="featured_image" class="form-label">Изображение карточки:</label>
                <select name="featured_image" id="featured_image" class="form-select" required>
                    <option value="" disabled selected>Выберите изображение</option>
                    {% for img in unused_images %}
                        <option value="img/{{ img }}">{{ img }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="mb-3">
                <label for="repository" class="form-label">Репозиторий в GitHub (URL):</label>
                <input type="text" name="repository" id="repository" class="form-control" required>
            </div>
            <div class="mb-4">
                <label for="semester" class="form-label">Семестр выполнения:</label>
                <div class="d-flex align-items-center">
                    <input type="range" id="semester" name="semester" class="form-range" min="1" max="8" step="1" value="1">
                    <span class="ms-3" id="semester-value">1</span>
                </div>
            </div>            <h3 class="mt-4">Работы:</h3>
            <div class="alert alert-info">
                <strong>Примечание:</strong> Блок "Выполненные работы" необязателен к заполнению. Если вы не добавите работы, этот раздел будет пустым.
            </div>
            <div class="mb-3">
                <label for="work-count" class="form-label">Количество работ:</label>
                <div class="input-group">
                    <input type="number" id="work-count" name="work_count" class="form-control" min="0" value="0">
                    <button type="button" id="generate-works" class="btn btn-secondary">Создать работы</button>
                </div>
            </div>
            <div id="works-container" class="mb-3"></div>

            <button type="submit" class="btn btn-primary w-100">Создать дисциплину</button>
        </form>
    </div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        var semesterSlider = document.getElementById('semester');
        var semesterValue = document.getElementById('semester-value');
        var worksContainer = document.getElementById('works-container');
        var generateWorksButton = document.getElementById('generate-works');

        // Устанавливаем начальное значение при загрузке страницы
        semesterValue.textContent = semesterSlider.value;

        // Обновляем отображение значения слайдера семестра
        semesterSlider.addEventListener('input', function() {
            semesterValue.textContent = semesterSlider.value;
        });        generateWorksButton.addEventListener('click', function() {
            var workCount = document.getElementById('work-count').value;
            worksContainer.innerHTML = ''; // Очищаем предыдущие поля
            
            if (workCount > 0) {
                for (var i = 0; i < workCount; i++) {
                    var newWork = document.createElement('div');
                    newWork.className = 'mb-3';
                    newWork.innerHTML = `
                        <div class="card mt-2">
                            <div class="card-body">
                                <h5 class="card-title">Работа ${i + 1}</h5>
                                <div class="mb-3">
                                    <label class="form-label">Название работы:</label>
                                    <input type="text" name="works[${i}][title]" class="form-control" placeholder="Лабораторная работа ${i + 1}">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Ссылка на работу:</label>
                                    <input type="url" name="works[${i}][link]" class="form-control" placeholder="https://disk.yandex.ru/i/...">
                                </div>
                            </div>
                        </div>
                    `;
                    worksContainer.appendChild(newWork);
                }
            } else {
                worksContainer.innerHTML = '<div class="alert alert-secondary">Работы не будут добавлены в дисциплину.</div>';
            }
        });
    });
</script>

</body>
</html>
    """, all_tags=parse_all_tags(), unused_images=get_unused_images())


@app.route('/create_discipline', methods=['POST'])
def create_discipline():
    # Ввод данных
    title = request.form['title']
    semester = request.form['semester']
    # Собираем выбранные чекбоксы
    selected_tags = request.form.getlist('existing_tags')
    # Новые теги из поля ввода
    new_tags = [t.strip() for t in request.form['tags'].split(',') if t.strip()]
    # Вычисляем год по семестру (1-2:2022, 3-4:2023, 5-6:2024, 7-8:2025)
    sem = int(semester)
    year = 2022 + (sem - 1) // 2
    # Новое формирование даты
    if sem % 2 == 1:
        date = f"{year}.01.01"
    else:
        date = f"{year}.07.01"
    # Генерируем slug автоматически
    slug = f"{translit(title)}-{semester}sem"
    author = "Клементьев Алексей Александрович"
    summary = request.form['summary']
    description = request.form.get('description', '').strip()
    featured_image = request.form['featured_image']  # теперь это путь вида img/filename
    repository = request.form['repository']
    work_count = int(request.form.get('work_count', 0))
    
    # Получение списка работ
    works = []
    for i in range(work_count):
        title_article = request.form.get(f'works[{i}][title]')
        link = request.form.get(f'works[{i}][link]')
        if title_article and link:
            works.append({'title': title_article, 'link': link})

    # Формируем путь к файлу
    filename = os.path.join(DISCIPLINES_DIR, f"{slug}.md")
      # Формируем содержание файла
    tags_list = [f"{semester} семестр"] + selected_tags + new_tags
    tags = ', '.join(sorted(set([t for t in tags_list if t])))
    
    content = f"""title: {title}
date: {date}
tags: {tags}
slug: {slug}
author: {author}
summary: {summary}
featured_image: {featured_image}
repository: {repository}

"""

    # Добавляем подробное описание, если оно есть
    if description:
        content += f"{description}\n\n"
    
    # Добавляем блок работ только если есть работы
    if works:
        content += "### Выполненные работы:\n"
        for work in works:
            content += f"- [{work['title']}]({work['link']})" + '{:target="_blank"}' + "\n"
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return f"Дисциплина '{title}' успешно создана! <a href='/'>Создать ещё одну</a>"


if __name__ == '__main__':
    if not os.path.exists(DISCIPLINES_DIR):
        os.makedirs(DISCIPLINES_DIR)
    
    app.run(debug=True, port=5000)
