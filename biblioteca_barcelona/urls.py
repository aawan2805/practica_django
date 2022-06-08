from django.urls import path
from biblioteca_barcelona import views

urlpatterns = [
    path('', views.Home.as_view(), name="login"),
]
