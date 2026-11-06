from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.pin_list, name="pin_list"),
    path("nuevo/", views.pin_create, name="pin_create"),
    path("pin/<int:pk>/", views.pin_detail, name="pin_detail"),
    path("pin/<int:pk>/puntuar/", views.pin_rate, name="pin_rate"),
    path("pin/<int:pk>/eliminar/", views.pin_delete, name="pin_delete"),
    path("u/<str:username>/", views.user_profile, name="profile"),
    path("registro/", views.signup, name="signup"),
    path("entrar/", auth_views.LoginView.as_view(), name="login"),
    path("salir/", auth_views.LogoutView.as_view(), name="logout"),
]
