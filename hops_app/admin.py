from django.contrib import admin
from .models import opintojaksot, valitut_kurssit, opinto_vuodet, toteutukset

#Viedään tietokantataulut damin näkymään
admin.site.register(opintojaksot)
admin.site.register(valitut_kurssit)
admin.site.register(opinto_vuodet)
admin.site.register(toteutukset)
