from django.urls import path, include
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='welcome_page'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('register_to_db', views.add_user_db, name='register_to_db'),
    path('', include('django.contrib.auth.urls')),
    path('homepage', views.my_view, name='myview'),
    path('manage_balance', views.income, name='income'),
    path('tweakbalance', views.tweakbalance, name='tweakbalance'),
    path('history_log', views.history_log, name="history_log"),
]
