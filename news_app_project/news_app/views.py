from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewsPreferencesForm

# Данные для демонстрации новостей
NEWS_DATA = {
    'politics': [
        {
            'title': 'Новые законы в сфере IT', 
            'date': '2024-01-15', 
            'summary': 'Обзор новых законодательных инициатив в цифровой экономике',
            'image': 'politics.webp'
        },
        {
            'title': 'Международные отношения', 
            'date': '2024-01-14', 
            'summary': 'Встреча глав государств по вопросам экономического сотрудничества',
            'image': 'politics.webp'
        },
    ],
    'sports': [
        {
            'title': 'Чемпионат по футболу', 
            'date': '2024-01-15', 
            'summary': 'Результаты матчей и турнирная таблица',
            'image': 'sports.webp'
        },
        {
            'title': 'Олимпийские игры', 
            'date': '2024-01-14', 
            'summary': 'Подготовка к соревнованиям и ожидаемые результаты',
            'image': 'sports.webp'
        },
    ],
    'technology': [
        {
            'title': 'Новый смартфон', 
            'date': '2024-01-15', 
            'summary': 'Анонс инновационного устройства с искусственным интеллектом',
            'image': 'technology.jpeg'
        },
        {
            'title': 'Искусственный интеллект', 
            'date': '2024-01-14', 
            'summary': 'Последние разработки в области машинного обучения',
            'image': 'technology.jpeg'
        },
    ],
    'entertainment': [
        {
            'title': 'Кино премьеры', 
            'date': '2024-01-15', 
            'summary': 'Новые фильмы в прокате с рейтингами критиков',
            'image': 'entertainment.webp'
        },
        {
            'title': 'Музыкальные новинки', 
            'date': '2024-01-14', 
            'summary': 'Вышел новый альбом популярного исполнителя',
            'image': 'entertainment.webp'
        },
    ],
    'business': [
        {
            'title': 'Курсы валют', 
            'date': '2024-01-15', 
            'summary': 'Анализ финансовых рынков и прогнозы экспертов',
            'image': 'business.webp'
        },
        {
            'title': 'Стартапы', 
            'date': '2024-01-14', 
            'summary': 'Успешные кейсы инвестиций и венчурного финансирования',
            'image': 'business.webp'
        },
    ],
    'health': [
        {
            'title': 'Медицинские исследования', 
            'date': '2024-01-15', 
            'summary': 'Новые методы лечения и клинические испытания',
            'image': 'health.webp'
        },
        {
            'title': 'Здоровый образ жизни', 
            'date': '2024-01-14', 
            'summary': 'Советы от экспертов по питанию и физической активности',
            'image': 'health.webp'
        },
    ]
}

# Mapping для фонов категорий
CATEGORY_BACKGROUNDS = {
    'politics': 'politics.webp',
    'sports': 'sports.webp', 
    'technology': 'technology.jpeg',
    'entertainment': 'entertainment.webp',
    'business': 'business.webp',
    'health': 'health.webp'
}
#render - функция для отображения HTML шаблонов

#redirect - функция для перенаправления на другие страницы

#HttpResponse - класс для простых текстовых ответов

#NewsPreferencesForm - наша форма из файла forms.py (импорт из текущей папки)

def set_cookie(response, key, value, days_expire=365):
    from django.utils.timezone import datetime, timedelta
     # Проверяем указан ли срок
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.strftime(datetime.now() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, secure=False, httponly=False)

# Функция настроек

def news_preferences(request):
    # Получаем текущие настройки из cookies
    current_theme = request.COOKIES.get('theme', 'light')
    current_language = request.COOKIES.get('language', 'ru')
    current_categories = request.COOKIES.get('categories', 'politics,sports,technology,entertainment,business,health').split(',')
    current_update_frequency = request.COOKIES.get('update_frequency', 'daily')
    current_email_notifications = request.COOKIES.get('email_notifications', 'false') == 'true'
    current_push_notifications = request.COOKIES.get('push_notifications', 'false') == 'true'
    
    # Получаем историю просмотров
    visited_pages = request.COOKIES.get('visited_pages', '').split(',')
    visited_pages = [page for page in visited_pages if page]

    # Проверяем отправлена ли форма
    if request.method == 'POST':
        form = NewsPreferencesForm(request.POST)
        # Проверяем корректны ли данные
        if form.is_valid():
            response = redirect('news_dashboard')
            
            # Сохраняем настройки в cookies
            set_cookie(response, 'theme', form.cleaned_data['theme'])
            set_cookie(response, 'language', form.cleaned_data['language'])
            set_cookie(response, 'categories', ','.join(form.cleaned_data['categories']))
            set_cookie(response, 'update_frequency', form.cleaned_data['update_frequency'])
            set_cookie(response, 'email_notifications', str(form.cleaned_data['email_notifications']).lower())
            set_cookie(response, 'push_notifications', str(form.cleaned_data['push_notifications']).lower())
            
            return response
    else:
        initial_data = {
            'theme': current_theme,
            'language': current_language,
            'categories': current_categories,
            'update_frequency': current_update_frequency,
            'email_notifications': current_email_notifications,
            'push_notifications': current_push_notifications,
        }
        form = NewsPreferencesForm(initial=initial_data)
    
    return render(request, 'news_app/preferences.html', {
        'form': form,
        'visited_pages': visited_pages[-5:],  # Последние 5 страниц
    })

  # update_frequency - настройка того, как часто пользователь хочет получать обновления новостей.
  # Эта функция вызывается когда пользователь заходит на главную страницу
    # request - содержит всю информацию о запросе (cookies, метод, данные и т.д.)

def news_dashboard(request):
    # Получаем настройки из cookies
    theme = request.COOKIES.get('theme', 'light')
    language = request.COOKIES.get('language', 'ru')
    
    # ПО УМОЛЧАНИЮ ВСЕ КАТЕГОРИИ
    selected_categories = request.COOKIES.get('categories', 'politics,sports,technology,entertainment,business,health').split(',')
    
    # Обновляем историю просмотров
    response = render(request, 'news_app/dashboard.html', {

        # Отображает данные
        'theme': theme,
        'language': language,
        'selected_categories': selected_categories,
        'news_data': NEWS_DATA,
    })
    
    # Сохраняем текущую страницу в историю
    visited_pages = request.COOKIES.get('visited_pages', '').split(',')
    visited_pages = [page for page in visited_pages if page]
    current_page = 'news_dashboard' 

    # Есть ли страница в списке посещеных страниц  
    if current_page not in visited_pages:
        visited_pages.append(current_page)
        # Соединяет все элементы списка visited_pages в одну строку
    if len(visited_pages) > 10:  
        visited_pages = visited_pages[-10:]

    # Установка значения в куки
    set_cookie(response, 'visited_pages', ','.join(visited_pages))
    return response

def category_news(request, category):
    if category not in NEWS_DATA:
        return redirect('news_dashboard')
    
    # Обновляем историю просмотров
    response = render(request, 'news_app/category.html', {
        'category': category,
        'news_items': NEWS_DATA[category],
        'theme': request.COOKIES.get('theme', 'light'),
        'category_background': CATEGORY_BACKGROUNDS.get(category, 'technology.jpg')
    })
    
    # Получаем историю из Cookies
    visited_pages = request.COOKIES.get('visited_pages', '').split(',')
    visited_pages = [page for page in visited_pages if page]
    current_page = f'category_{category}'
    if current_page not in visited_pages:
        visited_pages.append(current_page)
        # Если страниц больше 10, то оставляет последние 10
    if len(visited_pages) > 10:
        visited_pages = visited_pages[-10:]
    
    set_cookie(response, 'visited_pages', ','.join(visited_pages))
    return response
