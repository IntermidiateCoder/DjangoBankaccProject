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
    path('history_log', views.log_basic, name="history_log"),
    path('history_log/past_trans', views.past_trans, name="past_trans"),
    path('history_log/iograph', views.iograph, name="iograph"),
    path('history_log/balancegraph', views.balancegraph, name="balancegraph"),
    path('trans_chart_json', views.TransactionsView.as_view(), name="trans_chart_json"),
    path('balance_chart_json', views.BalanceView.as_view(), name="balance_chart_json"),
]
