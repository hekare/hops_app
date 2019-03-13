from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import opintojaksot, valitut_kurssit, opinto_vuodet, toteutukset
from django.db.models import Sum
from datetime import datetime
import json

#Aloitussivu
def start_page (request):
      if request.user.is_authenticated:
            return HttpResponseRedirect('home')
      if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                  login(request,user)
                  return HttpResponseRedirect('home')
      return render(request, 'login.html', {})

#Kirjaaminen ulos, ei poistamissivua
def user_logout (request):
      logout(request)
      return redirect('/')

#Uuden käyttäjän rekisteröinti sivu
def register(request):
      if request.user.is_authenticated:
            return HttpResponseRedirect('home')
      if request.method=='POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                  form.save()
                  username = form.cleaned_data.get("username")
                  password = form.cleaned_data.get("password1")
                  user = authenticate(username=username, password=password)
                  login(request, user)
                  return redirect('/')
      else:
            form = UserCreationForm()
      args = {'form': form}
      return render(request, 'register.html', args)

#Kirjautuneen käyttäjän aloitussivu
@login_required(login_url='/')
def home(request):
      try:
            vuosi = (opinto_vuodet.objects.filter(opiskelija=request.user).get()).opintovuosi
      except:
            vuosi = "Ei valittu"
      print(vuosi)
      args={
            'opintovuosi': vuosi,
      }
      return render(request, 'home.html', args)

#Aikataulusivun lataaminen
PERIODIAJAT = [["Sep 01","Oct 20"],["Oct 20","Dec 24"],["Jan 01","Mar 01"],["Mar 01","May 15"]]
@login_required(login_url='/')
def aikataulu(request):
      kurssi_nimet = list(valitut_kurssit.objects.filter(opiskelija=request.user).values_list("kurssi__koodi", flat=True))
      valitut__ = valitut_kurssit.objects.filter(opiskelija=request.user)
      valitut = []
      try:
            vuosi = (opinto_vuodet.objects.filter(opiskelija=request.user).get()).opintovuosi
      except:
            vuosi = "Ei valittu"

      today = datetime.today()

      for kurssi in valitut__:
            if(kurssi.periodi != None and kurssi.opinto_vuosi != None):
                  valitut.append([kurssi.kurssi.koodi, PERIODIAJAT[kurssi.periodi-1][0]+" 2013", PERIODIAJAT[kurssi.periodi-1][1]+" 2013"])

      
      args = {
            'nimet': json.dumps(kurssi_nimet),
            'valitut': json.dumps(valitut),
            'opintovuosi': vuosi,
      }
      return render(request, 'schedule_view.html', args)

#Listaus valituista kursseista sekä lista kursseita, joita on mahdollista valita
@login_required(login_url='/')
def lista(request):
      hakusana = None
      tuloksia = None
      lisays_onnistui = None
      haetut_kurssit = None

      #Valittavissa olevien kurssien hakeminen
      if request.method =="GET":
            query = request.GET.get("name_q")   
            if query:
                  haetut_kurssit = opintojaksot.objects.filter(nimi__icontains=query)
                  hakusana = query
                  tuloksia = len(haetut_kurssit)
            else:
                  haetut_kurssit = opintojaksot.objects.all().order_by('nimi')

      #Onko kurssi lisätty, vai onko jo lisätty
      if request.GET.get("added") == "0":
            lisays_onnistui = False
      elif request.GET.get("added") == "1":
            lisays_onnistui = True

      
      #Valittujen kurssien hakeminen
      '''
      nopat_perusopinnot = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="perusopinnot").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))

      nopat_pääaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="pääaine").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))

      nopat_sivuaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="sivuaine").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))

      nopat_valittavat = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="täydentävät").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))
      '''
      valitut_kurssit = hae_valitut_kurssit(request)
      nopat_sum = laske_nopat(request)

      #Opiskelijan oma opintovuosi
      try:
            vuosi = (opinto_vuodet.objects.filter(opiskelija=request.user).get()).opintovuosi
      except:
            vuosi = "Ei valittu"
      
      #argumenttien antaminen
      args={'kurssit': haetut_kurssit,
            'opintovuosi':vuosi,
            'haku': hakusana,
            'tuloksia': tuloksia,
            'lisays_onnistui': lisays_onnistui,
            'valitut': valitut_kurssit,
            'nopat': nopat_sum,
            }
      
      return render(request, 'list_view.html', args)


def hae_valitut_kurssit(request):
      #palautettava tietorakennen  käyttäjän valitsemista opinnoista
      valitut = {'perusopinnot':[],'pääaine':[],'sivuaine':[],'vapaat':[]}
      
      #perusopinnot
      perusopinnot = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="perusopinnot").order_by('kurssi')
      for kurssi in perusopinnot:
            tot = toteutukset.objects.filter(koodi=kurssi.kurssi).order_by('periodit')
            valitut['perusopinnot'].append([kurssi, tot])

      #pääaine
      pääaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="pääaine").order_by('kurssi')
      for kurssi in pääaine:
            tot = toteutukset.objects.filter(koodi=kurssi.kurssi).order_by('periodit')
            valitut['pääaine'].append([kurssi, tot])

      #sivuaine
      sivuaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="sivuaine").order_by('kurssi')
      for kurssi in sivuaine:
            tot = toteutukset.objects.filter(koodi=kurssi.kurssi).order_by('periodit')
            valitut['sivuaine'].append([kurssi, tot])

      #vapaasti valittavat
      vapaasti_valittavat = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="täydentävät").order_by('kurssi')
      for kurssi in vapaasti_valittavat:
            tot = toteutukset.objects.filter(koodi=kurssi.kurssi).order_by('periodit')
            valitut['vapaat'].append([kurssi, tot])
      
      return valitut

def laske_nopat(request):
      perusopinnot = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="perusopinnot").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))

      pääaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="pääaine").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))

      sivuaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="sivuaine").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))

      vapaat = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="täydentävät").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))
      nopat ={'perusopinnot':perusopinnot,'pääaine':pääaine,'sivuaine':sivuaine,'vapaat':vapaat}
      return nopat