from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_dashboard, name='news_dashboard'),
    path('preferences/', views.news_preferences, name='news_preferences'),
    path('category/<str:category>/', views.category_news, name='category_news'),
]