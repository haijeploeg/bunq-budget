from django.urls import path
from django.contrib.auth.views import LogoutView
from dashboard.views import DashboardView, AccountsView, TransactionsView, CategoryView, SavingsView, SettingsView, LoginView, RegisterView, TestView

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('accounts/', AccountsView.as_view(), name='accounts'),
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    path('category/', CategoryView.as_view(), name='category'),
    path('savings/', SavingsView.as_view(), name='savings'),
    path('account/settings', SettingsView.as_view(), name='settings'),
    path('test/', TestView.as_view(), name='test')
]
