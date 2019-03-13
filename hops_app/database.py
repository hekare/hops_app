from django.http import HttpResponseRedirect
from .models import opintojaksot, valitut_kurssit, opinto_vuodet, toteutukset
import json, requests
from django.http import HttpResponseRedirect, HttpResponse

#Funktio lataa yliopistun opintojaksot rajapinnasta ja siirtää tiedot tietokantaan.
def load_data(request):
      print("Updating data...")
      import os
      from django.conf import settings
      
      #Datan haku apista. Api palauttaa json-tiedoston kaikista keskustan kampuksen kursseista (tilanne 21.2.2019).
      headers = {'x-api-key':os.environ['X_API_KEY']}
      response = requests.get("https://opendata.uta.fi:8443/apiman-gateway/UTA/opintojaksot/1.0/", headers=headers)
      data = response.json()
      
      #datan siirto tietokantaan
      MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
      for kurssi in data:
            try:
                  #Tallenna opintojakso tietokantaan, jos olemassa -> päivitä kentät
                  opintojaksot.objects.create(
                        koodi = kurssi['code'],
                        nimi = kurssi['name'],
                        nopat_min = kurssi['creditsMin'],
                        nopat_max = kurssi['creditsMax'],
                        tutkinto_ohjelma = kurssi['degreeProgrammeCode'],
                        oppiaine = kurssi['subjectCode'],
                  )
            except:
                  #Päivitä opintojakson kentät
                  opintojaksot.objects.filter(koodi=kurssi['code']).update(
                        nimi = kurssi['name'],
                        nopat_min = kurssi['creditsMin'],
                        nopat_max = kurssi['creditsMax'],
                        tutkinto_ohjelma = kurssi['degreeProgrammeCode'],
                        oppiaine = kurssi['subjectCode'],
                  )

            #Toetutuksen kenttien muokkaus sopivaksi
            #Periodit merkkijonoksi muotoon alkuperiodi–loppuperiodi
            if(kurssi['studyPeriods'] == None or len(kurssi['studyPeriods']) == 0):
                  periodit = None
            elif(len(kurssi['studyPeriods']) == 1):
                  periodit = str(kurssi['studyPeriods'][0])
            else:
                  periodit = str(kurssi['studyPeriods'][0])+"–"+str(kurssi['studyPeriods'][-1])

            #Päivämäärä "YYYY-MM-DD" -> "MMM DD"
            startDate = MONTHS[int(kurssi['startDate'][5:-3])] + " " + kurssi['startDate'][-2:]
            endDate = MONTHS[int(kurssi['endDate'][5:-3])] + " " + kurssi['endDate'][-2:]
            
            if startDate != endDate: #Toteutuksen aikataulua ei tiedetä, joten ei lisätä toteutuksiin
                  #Toteutuskerran lisäys,jos olemassa -> päivitys
                  try:
                        toteutukset.objects.create(
                              tunniste = kurssi['id'],
                              koodi = opintojaksot.objects.filter(koodi=kurssi['code']).get(),
                              periodit = periodit,
                              aloituspvm = startDate,
                              lopetuspvm = endDate,
                        )
                  except:
                        toteutukset.objects.filter(tunniste=kurssi['id']).update(
                              koodi = opintojaksot.objects.filter(koodi=kurssi['code']).get(),
                              periodit = periodit,
                              aloituspvm = startDate,
                              lopetuspvm = endDate,
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
      kurssi = opintojaksot.objects.get(koodi=kurssi_id)
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
      if year == "None":
            year = None
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).update(opinto_vuosi=year)
      return HttpResponseRedirect("/list_view")

#Kurssin suoritusperiodin vaihtaminen
def select_period(request):
      toteutus = request.POST.get('periodi') #periodin id
      kurssi = request.POST.get("kurssi")
      if toteutus != "None":
            toteutus = toteutukset.objects.get(tunniste=toteutus)
      else:
            toteutus = None
      valitut_kurssit.objects.filter(opiskelija=request.user, kurssi=kurssi).update(toteutus=toteutus)
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