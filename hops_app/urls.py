from django.urls import path
from . import views, database

urlpatterns = [
      path('', views.start_page, name="start_page"),
      path('register', views.register, name="register"),
      path('logout', views.user_logout, name="logout"),
      path('home', views.home, name="home"),
      path('schedule_view', views.aikataulu, name="aikataulu"),
      path('list_view', views.lista, name="lista"),
      path('load_data', database.load_data, name="load_data"),
]