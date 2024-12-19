from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Путь к каталогу с файлами дисциплин
DISCIPLINES_DIR = 'content/posts'


@app.route('/')
def index():
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
                <label for="tags" class="form-label">Теги (навыки, ключевые слова через запятую):</label>
                <input type="text" name="tags" id="tags" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="slug" class="form-label">URL slug:</label>
                <input type="text" name="slug" id="slug" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="author" class="form-label">Автор:</label>
                <input type="text" name="author" id="author" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="summary" class="form-label">Краткое описание:</label>
                <input type="text" name="summary" id="summary" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="featured_image" class="form-label">Изображение карточки (URL):</label>
                <input type="text" name="featured_image" id="featured_image" class="form-control" required>
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
            </div>
            <div class="mb-4">
                <label for="date" class="form-label">Год выполнения:</label>
                <div class="d-flex align-items-center">
                    <input type="range" id="date" name="date" class="form-range" min="2021" max="2025" step="1" value="2021">
                    <span class="ms-3" id="date-value">2021</span>
                </div>
            </div>
            

            <h3 class="mt-4">Работы:</h3>
            <div class="mb-3">
                <label for="work-count" class="form-label">Количество работ:</label>
                <div class="input-group">
                    <input type="number" id="work-count" name="work_count" class="form-control" min="1" required>
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
        var dateSlider = document.getElementById('date');
        var dateValue = document.getElementById('date-value');
        var worksContainer = document.getElementById('works-container');
        var generateWorksButton = document.getElementById('generate-works');

        // Обновляем отображение значения слайдера семестра
        semesterSlider.addEventListener('input', function() {
            semesterValue.textContent = semesterSlider.value;
        });

        // Обновляем отображение значения слайдера даты
        dateSlider.addEventListener('input', function() {
            dateValue.textContent = dateSlider.value;
        });

        generateWorksButton.addEventListener('click', function() {
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
                                    <input type="text" name="works[${i}][title]" class="form-control" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Ссылка на работу:</label>
                                    <input type="url" name="works[${i}][link]" class="form-control" required>
                                </div>
                            </div>
                        </div>
                    `;
                    worksContainer.appendChild(newWork);
                }
            }
        });
    });
</script>

</body>
</html>
    """)


@app.route('/create_discipline', methods=['POST'])
def create_discipline():
    # Ввод данных
    title = request.form['title']
    semester = request.form['semester']  # Включение семестра
    tags = f"{semester} семестр, {request.form['tags']}".replace(", ", ", ")
    date = request.form['date']
    date = f"{date}.01.01"
    slug = request.form['slug']
    author = request.form['author']
    summary = request.form['summary']
    featured_image = request.form['featured_image']
    repository = request.form['repository']
    work_count = int(request.form['work_count'])
    
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
    content = f"""title: {title}
date: {date}
tags: {tags}
slug: {slug}
author: {author}
summary: {summary}
featured_image: {featured_image}
repository: {repository}

### Выполненные работы:
"""

    if works:
        for work in works:
            content += f"- [{work['title']}]({work['link']})\n"
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return f"Дисциплина '{title}' успешно создана! <a href='/'>Создать ещё одну</a>"


if __name__ == '__main__':
    if not os.path.exists(DISCIPLINES_DIR):
        os.makedirs(DISCIPLINES_DIR)
    
    app.run(debug=True, port=5000)
