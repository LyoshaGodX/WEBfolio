#!/usr/bin/env powershell
# -*- coding: utf-8 -*-
"""
PowerShell скрипт для автоматической сборки сайта с обновлением тегов
"""

Write-Host "🔄 Автоматическое обновление и сборка сайта..." -ForegroundColor Cyan
Write-Host "=" * 60

# Обновляем теги навыков
Write-Host "📊 Обновление тегов навыков..." -ForegroundColor Yellow
python update_skills_tags.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Теги успешно обновлены!" -ForegroundColor Green
    
    # Собираем сайт
    Write-Host "`n🏗️ Сборка сайта..." -ForegroundColor Yellow
    make html
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Сайт успешно собран!" -ForegroundColor Green
        Write-Host "`n🌐 Сайт готов к просмотру в папке 'output'" -ForegroundColor Cyan
        Write-Host "=" * 60
        
        # Показываем статистику
        $postCount = (Get-ChildItem "content/posts" -Filter "*.md").Count
        $skillsCount = (python -c "from pelicanconf import SKILLS_TAGS; print(len(SKILLS_TAGS))")
        
        Write-Host "📈 Статистика:" -ForegroundColor Magenta
        Write-Host "   • Дисциплин: $postCount" -ForegroundColor White
        Write-Host "   • Навыков/технологий: $skillsCount" -ForegroundColor White
        Write-Host "=" * 60
    } else {
        Write-Host "❌ Ошибка при сборке сайта!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Ошибка при обновлении тегов!" -ForegroundColor Red
    exit 1
}