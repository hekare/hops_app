from django.urls import path
from . import views, db

urlpatterns = [
      path('', views.start_page, name="start_page"),
      path('register', views.register, name="register"),
      path('logout', views.user_logout, name="logout"),
      path('home', views.home, name="home"),
      path('aikataulu', views.aikataulu, name="aikataulu"),
      path('lista', views.lista, name="lista"),
      path('load_data', db.load_data, name="load_data"),
]