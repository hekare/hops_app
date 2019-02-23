from django.urls import path
from . import views, database

urlpatterns = [
      path('', views.start_page, name="start_page"),
      path('register', views.register, name="register"),
      path('logout', views.user_logout, name="logout"),
      path('home', views.home, name="home"),
      path('schedule_view/', views.aikataulu, name="aikataulu"),
      path('list_view/', views.lista, name="lista"),
      path('list_view/remove', database.remove_course, name="remove_course"),
      path('list_view/add', database.add_course, name="add_course"),
      path('load_data', database.load_data, name="load_data"),
      path('delete_data', database.clear_database, name="delete_data"),
]