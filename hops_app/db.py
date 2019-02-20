from django.http import HttpResponseRedirect
from .models import opintojaksot
import json, requests

def load_data(request):
      #Funktio lataa yliopistun opintojaksot rajapinnasta ja siirtää tiedot tietokantaan.
      print("Updating data...")

      #apin avaimen haku
      secret_file = open('../secrets.json')
      secrets = json.load(secret_file)
      secret_file.close()

      #datan haku apista
      headers = {'x-api-key':secrets['X-API-KEY']}
      response = requests.get("https://opendata.uta.fi:8443/apiman-gateway/UTA/opintojaksot/1.0/", headers=headers)
      data = response.json()
      
      #datan siirto tietokantoihin
      #print(data[1]['id'])
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