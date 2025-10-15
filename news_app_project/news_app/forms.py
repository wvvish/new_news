from django import forms

class NewsPreferencesForm(forms.Form):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
    ]
    
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'English'),
    ]
    
    CATEGORY_CHOICES = [
        ('politics', 'Политика'),
        ('sports', 'Спорт'),
        ('technology', 'Технологии'),
        ('entertainment', 'Развлечения'),
        ('business', 'Бизнес'),
        ('health', 'Здоровье'),
    ]
    
    # Настройки темы и языка
    theme = forms.ChoiceField(
        choices=THEME_CHOICES,
        widget=forms.RadioSelect,
        label='Тема оформления'
    )
    
    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        widget=forms.RadioSelect,
        label='Язык интерфейса'
    )
    
    # Категории новостей
    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Интересующие категории',
        required=True
    )
    
    # Частота обновления
    update_frequency = forms.ChoiceField(
        choices=[
            ('realtime', 'В реальном времени'),
            ('hourly', 'Каждый час'),
            ('daily', 'Ежедневно'),
        ],
        label='Частота обновления'
    )
    
    # Уведомления
    email_notifications = forms.BooleanField(
        required=False,
        label='Email уведомления'
    )
    
    push_notifications = forms.BooleanField(
        required=False,
        label='Push уведомления'
    )