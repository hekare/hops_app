from django.http import HttpResponseRedirect
from .models import opintojaksot, valitut_kurssit
import json, requests
from django.http import HttpResponseRedirect, HttpResponse

def load_data(request):
      #Funktio lataa yliopistun opintojaksot rajapinnasta ja siirtää tiedot tietokantaan.
      print("Updating data...")

      #apin avaimen haku
      secret_file = open('../secrets.json')
      secrets = json.load(secret_file)
      secret_file.close()

      #Datan haku apista. Api palauttaa json-tiedoston kaikista keskustan kampuksen kursseista (tilanne 21.2.2019).
      headers = {'x-api-key':secrets['X-API-KEY']}
      response = requests.get("https://opendata.uta.fi:8443/apiman-gateway/UTA/opintojaksot/1.0/", headers=headers)
      data = response.json()
      
      #datan siirto tietokantaan
      for kurssi in data:
            p1 = False
            p2 = False
            p3 = False
            p4 = False
            p5 = False
            if kurssi['studyPeriods']!= None:
                  if 1 in kurssi['studyPeriods']:
                        p1 = True 
                  if 2 in kurssi['studyPeriods']:
                        p2 = True 
                  if 3 in kurssi['studyPeriods']:
                        p3 = True 
                  if 4 in kurssi['studyPeriods']:
                        p4 = True 
                  if 5 in kurssi['studyPeriods']:
                        p5 = True 

            #Tallenna tietokantaan, jos olemassa -> päivitä kentät
            opintojaksot.objects.update_or_create(
                  tunniste = kurssi['id'],
                  koodi = kurssi['code'],
                  nimi = kurssi['name'],
                  pisteet_min = kurssi['creditsMin'],
                  pisteet_max = kurssi['creditsMax'],
                  tutkinto_ohjelma = kurssi['degreeProgrammeCode'],
                  oppiaine = kurssi['subjectCode'],
                  periodi1 = p1,
                  periodi2 = p2,
                  periodi3 = p3,
                  periodi4 = p4,
                  periodi5 = p5,
            )

      print("Data updatet")
      return HttpResponseRedirect('home')

def remove_course(request):
      kurssi_id = request.POST.get("remove")
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi_id).delete()
      return HttpResponseRedirect("/list_view")

def add_course(request):
      add = request.POST.get("add")
      try:
            valitut_kurssit.objects.create(opiskelija=request.user, kurssi=request.POST.get('add'))
            url = "/list_view/?added=1"
      except:
            url = "/list_view/?added=0"
      return HttpResponseRedirect(url)