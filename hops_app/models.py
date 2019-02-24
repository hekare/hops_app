from django.db import models
from django.contrib.auth.models import User
import json

class opintojaksot (models.Model):
      tunniste = models.CharField(max_length=20, primary_key=True) #id, numero – ei kerro mitään
      koodi = models.CharField(max_length=20) #kurrsin koodi – kurssin lyhenne
      nimi = models.TextField()
      nopat_min = models.IntegerField()
      nopat_max = models.IntegerField()
      tutkinto_ohjelma = models.CharField(max_length=20, null=True)
      oppiaine = models.CharField(max_length=20, null=True)
      periodit = models.CharField(max_length=20, null=True) #string muotoinen lista kursseista
      def __str__(self):
            return self.nimi
      def get_periodit(self): #palauttaa periodit listana
            if self.periodit == None:
                  return None
            return self.periodit.replace("[", "").replace("]", "").split(",")
      class Meta:
            verbose_name_plural = "Opintojaksot"

class valitut_kurssit (models.Model):
      opiskelija = models.ForeignKey(User, on_delete=models.CASCADE)
      kurssi = models.ForeignKey(opintojaksot, on_delete=models.CASCADE) #opintojakson id
      periodi = models.IntegerField(null=True)
      opinto_vuosi = models.IntegerField(null=True)
      def __str__(self):
            return self.opiskelija.username
      class Meta:
            verbose_name_plural = "Valitut kurssit"
            unique_together = (("opiskelija", "kurssi"),)