from django.urls import path

from .views import TeamView, LoginView

urlpatterns = [
    path('team', TeamView.as_view(), name='team'),
    path('login', LoginView.as_view(), name='login'),
]