from django.urls import path
from users import views

app_name = "users"


urlpatterns = [
    path("", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("register/", views.register, name='register'),
    path("home/", views.index, name='index'),
]
