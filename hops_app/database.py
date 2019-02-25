from django.http import HttpResponseRedirect
from .models import opintojaksot, valitut_kurssit
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

def clear_database(requests):
      opintojaksot.objects.all().delete()
      return HttpResponseRedirect('home')

def remove_course(request):
      kurssi = request.POST.get("remove")
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).delete()
      return HttpResponseRedirect("/list_view")

def add_course(request):
      kurssi_id = request.POST.get('add')
      kurssi = opintojaksot.objects.get(tunniste=kurssi_id)
      try:
            valitut_kurssit.objects.create(opiskelija=request.user, kurssi=kurssi)
            url = "/list_view/?added=1"
      except:
           url = "/list_view/?added=0"
      return HttpResponseRedirect(url)

def change_year(request):
      year = request.POST.get("vuosi")
      kurssi = request.POST.get("kurssi")
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).update(opinto_vuosi=year)
      return HttpResponseRedirect("/list_view")

def select_period(request):
      period = request.POST.get('periodi')
      kurssi = request.POST.get("kurssi")
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).update(periodi=period)
      return HttpResponseRedirect("/list_view")


def select_module(request):
      module = request.POST.get('moduuli')
      kurssi = request.POST.get('kurssi')
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).update(opintokokonaisuus=module)
      return HttpResponseRedirect("/list_view")