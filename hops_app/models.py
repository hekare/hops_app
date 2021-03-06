from django.db import models
from django.contrib.auth.models import User
import json

#Opintojaksot/kurssit
class opintojaksot (models.Model):
      #tunniste = models.CharField(max_length=20, primary_key=True) #id, numero – ei kerro mitään
      #koodi = models.CharField(max_length=20) #kurrsin koodi – kurssin lyhenne
      koodi = models.CharField(max_length=20, primary_key=True) #kurrsin koodi – kurssin lyhenne
      nimi = models.TextField()
      nopat_min = models.IntegerField()
      nopat_max = models.IntegerField()
      tutkinto_ohjelma = models.CharField(max_length=20, null=True)
      oppiaine = models.CharField(max_length=20, null=True)
      #periodit = models.CharField(max_length=20, null=True) #string muotoinen lista kursseista
      def __str__(self):
            return self.nimi
      class Meta:
            verbose_name_plural = "Opintojaksot"

#Opintojaksojen toteutukset
class toteutukset (models.Model):
      tunniste = models.CharField(max_length=20, primary_key=True) #id, numero – ei kerro mitään
      koodi = models.ForeignKey(opintojaksot, on_delete=models.CASCADE) #kurrsin koodi – kurssin lyhenne
      periodit = models.CharField(max_length=3, null=True)
      aloituspvm = models.CharField(max_length=10, null=True)
      lopetuspvm = models.CharField(max_length=10, null=True)
      def __str__(self):
            return "{0}: periodeissa {1}".format(self.koodi, self.periodit)
      class Meta:
            verbose_name_plural = "Opintojaksojen toteutukset"

#Käyttäjien valitsemat kurssit
class valitut_kurssit (models.Model):
      opiskelija = models.ForeignKey(User, on_delete=models.CASCADE)
      kurssi = models.ForeignKey(opintojaksot, on_delete=models.CASCADE) #opintojakson id
      toteutus = models.ForeignKey(toteutukset, on_delete=models.CASCADE, null=True)
      opinto_vuosi = models.IntegerField(null=True)
      opintokokonaisuus = models.CharField(max_length=20, default="täydentävät")
      def __str__(self):
            return "{0}: {1}".format(self.opiskelija.username, self.kurssi.nimi)
      def get_modules(self):
            return ["perusopinnot","pääaine","sivuaine","täydentävät"]
      class Meta:
            verbose_name_plural = "Valitut kurssit"
            unique_together = (("opiskelija", "kurssi"),)

#Kyttäjien kuluvat opintovuodet
class opinto_vuodet (models.Model):
      opiskelija = models.ForeignKey(User, on_delete=models.CASCADE)
      opintovuosi = models.IntegerField(null=True)
      def __str__(self):
            return self.opiskelija.username
      class Meta:
            verbose_name_plural = "Opinto vuodet"