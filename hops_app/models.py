from django.db import models

class opintojaksot (models.Model):
      tunniste = models.CharField(max_length=20, primary_key=True) #id, numero – ei kerro mitään
      koodi = models.CharField(max_length=20) #kurrsin koodi – kurssin lyhenne
      nimi = models.TextField()
      nopat_min = models.IntegerField()
      nopat_max = models.IntegerField()

class periodit (models.Model):
      opintojakso = models.CharField(max_length=20, primary_key=True) #opintojakson tunniste
      periodi1 = models.BooleanField(default=False)
      periodi2 = models.BooleanField(default=False)
      periodi3 = models.BooleanField(default=False)
      periodi4 = models.BooleanField(default=False)
      periodi5 = models.BooleanField(default=False)

class tutkinto_ohjelmat (models.Model):
      koodi = models.CharField(max_length=20, primary_key=True) #tutkinto-ohjelman koodi
      opintojakso = models.CharField(max_length=20,) #opintojakson tunniste

class oppi_aineet (models.Model):
      koodi = models.CharField(max_length=20, primary_key=True) #oppiaineen koodi
      opintojakso = models.CharField(max_length=20) #opintojakson tunniste