from django.urls import path
from . import views, database

urlpatterns = [
      #Sivujen latauspyynnöt
      path('', views.start_page, name="start_page"),
      path('register', views.register, name="register"),
      path('logout', views.user_logout, name="logout"),
      path('home', views.home, name="home"),
      path('schedule_view/', views.aikataulu, name="aikataulu"),
      path('list_view/', views.lista, name="lista"),

      #Tietokantaa muuttavat POST pyynnöt
      path('list_view/remove', database.remove_course, name="remove_course"), #Kurssivalinnan poistaminen
      path('list_view/add', database.add_course, name="add_course"), #Kurssivalinnan lisääminen
      path('list_view/change_year', database.change_year, name="change_year"), #Kurssin suoritusvuoden vaihtaminen
      path('list_view/select_period', database.select_period, name="select_pariod"), #Kurssin suoritusperiodin vaihtaminen
      path('list_view/select_module', database.select_module, name="select_module"), #Kurssin sisällyttäminen haluttuun opintokokonaisuuteen
      path('load_data', database.load_data, name="load_data"), #Datan lataaminen tietokantaan rajapinnasta
      path('delete_data', database.clear_database, name="delete_data"), #Opintojaksot taulun tyhjentäminen
      path('oma_vuosi', database.own_study_year, name="oma_vuosi") #Opiskelijan oman vuoden vaihtaminen
]