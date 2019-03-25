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
      args={
            'opintovuosi': vuosi,
      }
      return render(request, 'home.html', args)

#Aikataulusivun lataaminen
@login_required(login_url='/')
def aikataulu(request):
      kurssi_nimet = list(valitut_kurssit.objects.filter(opiskelija=request.user).values_list("kurssi__koodi", flat=True))
      valitut_toteutukset = valitut_kurssit.objects.filter(opiskelija=request.user)
      valitut = []
      try:
            vuosi = int((opinto_vuodet.objects.filter(opiskelija=request.user).get()).opintovuosi)
      except:
            vuosi = "Ei valittu"

      today = datetime.today()

      for kurssi in valitut_toteutukset:
            if(kurssi.toteutus != None and kurssi.opinto_vuosi != None):
                  start = datetime.strptime(kurssi.toteutus.aloituspvm, "%b %d")
                  end = datetime.strptime(kurssi.toteutus.lopetuspvm, "%b %d")
                  if today.month >=7:
                        if start.month >= 7:
                              vuosiStart = today.year
                        else:
                              vuosiStart = today.year + 1
                        if end.month >= 7:
                              vuosiEnd = today.year
                        else:
                              vuosiEnd = today.year +1
                  else:
                        if start.month > 7:
                              vuosiStart = today.year - 1 
                        else:
                              vuosiStart = today.year
                        if end.month >= 7:
                              vuosiEnd = today.year - 1
                        else:
                              vuosiEnd = today.year
                  
                  erotus = kurssi.opinto_vuosi - vuosi
                  vuosiEnd += erotus
                  vuosiStart += erotus
                  valitut.append([kurssi.kurssi.koodi, kurssi.toteutus.aloituspvm+" "+str(vuosiStart), kurssi.toteutus.lopetuspvm+ " "+str(vuosiEnd), (kurssi.opintokokonaisuus).replace("ä", "a"), kurssi.kurssi.nimi])
      
      nopat = valitut_kurssit.objects.filter(opiskelija=request.user).aggregate(Sum('kurssi__nopat_max'))
      args = {
            'nimet': json.dumps(kurssi_nimet),
            'valitut': json.dumps(valitut),
            'opintovuosi': vuosi,
            'noppia': nopat["kurssi__nopat_max__sum"],
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