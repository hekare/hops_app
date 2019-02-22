from django.db import models
from django.contrib.auth.models import User

class opintojaksot (models.Model):
      tunniste = models.CharField(max_length=20, primary_key=True) #id, numero – ei kerro mitään
      koodi = models.CharField(max_length=20) #kurrsin koodi – kurssin lyhenne
      nimi = models.TextField()
      nopast_min = models.IntegerField()
      nopat_max = models.IntegerField()
      tutkinto_ohjelma = models.CharField(max_length=20, null=True)
      oppiaine = models.CharField(max_length=20, null=True)
      periodi1 = models.BooleanField(default=False)
      periodi2 = models.BooleanField(default=False)
      periodi3 = models.BooleanField(default=False)
      periodi4 = models.BooleanField(default=False)
      periodi5 = models.BooleanField(default=False)
      def __str__(self):
            return self.nimi
      class Meta:
            verbose_name_plural = "Opintojaksot"

class valitut_kurssit (models.Model):
      opiskelija = models.ForeignKey(User, on_delete=models.CASCADE)
      kurssi = models.CharField(max_length=20, null=True) #opintojakson id
      periodi = models.IntegerField(null=True)
      opinto_vuosi = models.IntegerField(null=True)
      def __str__(self):
            return self.opiskelija.username
      class Meta:
            verbose_name_plural = "Valitut kurssit"
            unique_together = (("opiskelija", "kurssi"),)