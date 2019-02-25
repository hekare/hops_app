from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import opintojaksot, valitut_kurssit
from django.db.models import Sum


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

def user_logout (request):
      logout(request)
      return redirect('/')

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

@login_required(login_url='/')
def home(request):
      return render(request, 'home.html', {})

@login_required(login_url='/')
def aikataulu(request):
      return render(request, 'schedule_view.html', {})

@login_required(login_url='/')
def lista(request):
      hakusana = None
      tuloksia = None
      lisays_onnistui = None
      haetut_kurssit = None

      if request.method =="GET":
            query = request.GET.get("name_q")   
            if query:
                  haetut_kurssit = opintojaksot.objects.filter(nimi__icontains=query)
                  hakusana = query
                  tuloksia = len(haetut_kurssit)
            else:
                  haetut_kurssit = opintojaksot.objects.all().order_by('nimi')

      if request.GET.get("added") == "0":
            lisays_onnistui = False
      elif request.GET.get("added") == "1":
            lisays_onnistui = True

      perusopinnot = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="perusopinnot").order_by('kurssi')
      nopat_perusopinnot = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="perusopinnot").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))
      pääaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="pääaine").order_by('kurssi')
      nopat_pääaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="pääaine").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))
      sivuaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="sivuaine").order_by('kurssi')
      nopat_sivuaine = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="sivuaine").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))
      vapaasti_valittavat = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="täydentävät").order_by('kurssi')
      nopat_valittavat = valitut_kurssit.objects.filter(opiskelija=request.user, opintokokonaisuus="täydentävät").aggregate(Sum('kurssi__nopat_min'), Sum('kurssi__nopat_max'))
      
      args={'kurssit': haetut_kurssit,
            'haku': hakusana, 
            'tuloksia': tuloksia, 
            'lisays_onnistui': lisays_onnistui,
            'perusopinnot': [perusopinnot, nopat_perusopinnot['kurssi__nopat_min__sum'], nopat_perusopinnot['kurssi__nopat_min__sum']],
            'pääaine': [pääaine, nopat_pääaine['kurssi__nopat_min__sum'], nopat_pääaine['kurssi__nopat_min__sum']],
            'sivuaine': [sivuaine, nopat_sivuaine['kurssi__nopat_min__sum'], nopat_sivuaine['kurssi__nopat_min__sum']],
            'vapaasti_valittavat': [vapaasti_valittavat, nopat_valittavat['kurssi__nopat_min__sum'], nopat_valittavat['kurssi__nopat_min__sum']],
            }
      
      return render(request, 'list_view.html', args)