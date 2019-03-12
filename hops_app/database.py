from django.http import HttpResponseRedirect
from .models import opintojaksot, valitut_kurssit, opinto_vuodet
import json, requests
from django.http import HttpResponseRedirect, HttpResponse

def load_data(request):
      #Funktio lataa yliopistun opintojaksot rajapinnasta ja siirtää tiedot tietokantaan.
      print("Updating data...")
      import os
      from django.conf import settings
      
      #Datan haku apista. Api palauttaa json-tiedoston kaikista keskustan kampuksen kursseista (tilanne 21.2.2019).
      headers = {'x-api-key':os.environ['X_API_KEY']}
      response = requests.get("https://opendata.uta.fi:8443/apiman-gateway/UTA/opintojaksot/1.0/", headers=headers)
      data = response.json()
      
      #datan siirto tietokantaan
      for kurssi in data:
            #Tallenna tietokantaan, jos olemassa -> päivitä kentät
            try:
                  opintojaksot.objects.create(
                        tunniste = kurssi['id'],
                        koodi = kurssi['code'],
                        nimi = kurssi['name'],
                        nopat_min = kurssi['creditsMin'],
                        nopat_max = kurssi['creditsMax'],
                        tutkinto_ohjelma = kurssi['degreeProgrammeCode'],
                        oppiaine = kurssi['subjectCode'],
                        periodit = kurssi['studyPeriods'],
                  )
            except:
                  opintojaksot.objects.filter(tunniste=kurssi['id']).update(
                        koodi = kurssi['code'],
                        nimi = kurssi['name'],
                        nopat_min = kurssi['creditsMin'],
                        nopat_max = kurssi['creditsMax'],
                        tutkinto_ohjelma = kurssi['degreeProgrammeCode'],
                        oppiaine = kurssi['subjectCode'],
                        periodit = kurssi['studyPeriods'],
                  )
      print("Data updatet")
      return HttpResponseRedirect('home')

#Opintojaksot taulun tyhjentäminen
def clear_database(requests):
      opintojaksot.objects.all().delete()
      return HttpResponseRedirect('home')

#Valitun kurssin poistaminen käyttäjän valinnoista
def remove_course(request):
      kurssi = request.POST.get("remove")
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).delete()
      return HttpResponseRedirect("/list_view")

#Kurssivalinnan lisääminen käyttäjän kursseihin
def add_course(request):
      kurssi_id = request.POST.get('add')
      kurssi = opintojaksot.objects.get(tunniste=kurssi_id)
      try:
            valitut_kurssit.objects.create(opiskelija=request.user, kurssi=kurssi)
            url = "/list_view/?added=1"
      except:
           url = "/list_view/?added=0"
      return HttpResponseRedirect(url)

#Kurssin suoritusvuoden vaihtaminen
def change_year(request):
      year = request.POST.get("vuosi")
      kurssi = request.POST.get("kurssi")
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).update(opinto_vuosi=year)
      return HttpResponseRedirect("/list_view")

#Kurssin suoritusperiodin vaihtaminen
def select_period(request):
      period = request.POST.get('periodi')
      kurssi = request.POST.get("kurssi")
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).update(periodi=period)
      return HttpResponseRedirect("/list_view")

#Kurssin sisällyttäminen haluttuun opintokokonaisuuteen
def select_module(request):
      module = request.POST.get('moduuli')
      kurssi = request.POST.get('kurssi')
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).update(opintokokonaisuus=module)
      return HttpResponseRedirect("/list_view")

#Opiskelijan oman opintovuoden vaihtaminen
def own_study_year(request):
      vuosi = request.POST.get('vuosi')
      opinto_vuodet.objects.get_or_create(opiskelija=request.user)
      opinto_vuodet.objects.filter(opiskelija=request.user).update(opintovuosi=vuosi)
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))