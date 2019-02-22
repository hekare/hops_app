from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import opintojaksot, valitut_kurssit


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
      haku = None
      tuloksia = None
      lisays_onnistui = None

      if request.method=="GET":
            query = request.GET.get("name_q")
            if query:
                  kurssit = opintojaksot.objects.filter(nimi__icontains=query)
                  haku = query
                  tuloksia = len(kurssit)
            else:
                  kurssit = opintojaksot.objects.all().order_by('nimi')
      elif request.method=="POST":
            add = request.POST.get("add")
            try:
                  valitut_kurssit.objects.create(opiskelija=request.user, kurssi=add)
                  lisays_onnistui = True
            except:
                  lisays_onnistui = False
            kurssit = opintojaksot.objects.all().order_by('nimi')
      
      valitut_opintojaksot = valitut_kurssit.objects.filter(opiskelija=request.user)
      args={'kurssit': kurssit,
            'haku': haku, 
            'tuloksia': tuloksia, 
            'lisays_onnistui': lisays_onnistui,
            'valitut': valitut_opintojaksot}
      return render(request, 'list_view.html', args)