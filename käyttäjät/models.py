from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import now



class Asiakas(models.Model):
    käyttäjä = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    yritys = models.CharField(max_length=200, null=True)
    tilaaja = models.CharField(max_length=200, null=True, blank=True)
    puhelin = models.CharField(max_length=200, null=True, blank=True)
    sähköposti = models.CharField(max_length=200, null=True, blank=True)
    lisätty = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.yritys

    class Meta:
        verbose_name_plural = "Yrityslista"   


class TyöKohde(models.Model):
    kohde = models.CharField(max_length=200, null=True)
    osoite = models.CharField(max_length=200, null=True, blank=True)
    postinumero = models.CharField(max_length=10, null=True, blank=True)
    postitoimipaikka = models.CharField(max_length=200, null=True, blank=True)
    yhteyshenkilö = models.CharField(max_length=200, null=True, blank=True)
    nimike = models.CharField(max_length=200, null=True, blank=True)
    puhelin = models.CharField(max_length=200, null=True, blank=True)
    lisätty = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.kohde
    
    class Meta:
        verbose_name_plural = "Työ kohteet"   
    


class Laskutustiedot(models.Model):
    yritys = models.CharField(max_length=200, null=True)
    osoite = models.CharField(max_length=200, null=True, blank=True)
    postinumero = models.CharField(max_length=10, null=True, blank=True)
    postitoimipaikka = models.CharField(max_length=200, null=True, blank=True)
    yhteyshenkilö = models.CharField(max_length=200, null=True, blank=True)
    nimike = models.CharField(max_length=200, null=True, blank=True)
    puhelin = models.CharField(max_length=200, null=True, blank=True)
    lisätty = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.yritys
        
    class Meta:
        verbose_name_plural = "Laskutustiedot"   


from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
    
from django_currentuser.db.models import CurrentUserField




class Tilaus(models.Model):
    
    TILA = (
        ('Jonossa', 'Jonossa'),
        ('Työn alla', 'Työn alla'),
        ('Valmis', 'Valmis')
    )
    TYÖ = (
        ('Asennus', 'Asennus'),
        ('Huolto', 'Huolto'),
        ('Koulutus', 'Koulutus'),
        ('Ohjelmointi', 'Ohjelmointi'),
        ('Remontti', 'Remontti'),
        ('Konsultointi', 'Konsultointi'),
        ('Muu', 'Muu')
    )
    JÄRJESTELMÄ = (
        ('Rikosilmoitinjärjestelmä', 'Rikosilmoitinjärjestelmä'),
        ('Videovalvontajärjestelmä', 'Videovalvontajärjestelmä'),
        ('Kulunvalvontajärjestelmä', 'Kulunvalvontajärjestelmä'),
        ('Ilmoituksensiirtojärjestelmä', 'Ilmoituksensiirtojärjestelmä'),
        ('TV-järjestelmä', 'TV-järjestelmä'),
        ('Äänentoistojärjestelmä', 'Äänentoistojärjestelmä'),
        ('Kuulutusjärjestelmä', 'Kuulutusjärjestelmä'),
        ('Ovipuhelinjärjestelmä', 'Ovipuhelinjärjestelmä'),
        ('Pikapuhelinjärjestelmä', 'Pikapuhelinjärjestelmä'),
        ('Kiinteistö', 'Kiinteistö'),
        ('Ovikellojärjestelmä', 'Ovikellojärjestelmä'),
        ('Sähköjärjestelmä', 'Sähköjärjestelmä'),
        ('Info-TV järjestelmä', 'Info-TV järjestelmä'),
        ('Heikkovirtajärjestelmä', 'Heikkovirtajärjestelmä'),
        ('ATK-järjestelmä', 'ATK-järjestelmä'),
        ('Korjausrakentaminen', 'Korjausrakentaminen'),
        ('Tuotesuojajärjestelmä', 'Tuotesuojajärjestelmä'),
        ('Lukitusjärjestelmä', 'Lukitusjärjestelmä'),
        ('Kiinteistoautomatiikkajärjestelmä', 'Kiinteistoautomatiikkajärjestelmä'),
        ('Palovaroitinjärjestelmä', 'Palovaroitinjärjestelmä'),
        ('Kylmälaite', 'Kylmälaite'),
        ('Paloilmoitinjärjestelmä', 'Paloilmoitinjärjestelmä'),
        ('Antennijärjestelmä', 'Antennijärjestelmä'),
        ('Purunpoistojärjestelmä', 'Purunpoistojärjestelmä'),
        ('Muu', 'Muu'),
    )
    LUOKKA = (
        ('Normaali', 'Normaali'),
        ('Kiireinen', 'Kiireinen'),
        ('Päivystystyö', 'Päivystystyö')
    )
    LASKUTETTU = (
        ('Ei', 'Ei'),
        ('Kyllä', 'Kyllä')
        )
    

    asiakas = models.ForeignKey(Asiakas, null=True, on_delete= models.SET_NULL)
    työkohde = models.ForeignKey(TyöKohde, null=True, on_delete= models.SET_NULL)
    laskutustiedot = models.ForeignKey(Laskutustiedot, null=True, on_delete= models.SET_NULL)
    tilauspäivä = models.DateField(default=now, blank=True)
    merkinne = models.CharField(max_length=200, null=True, blank=True)
    tila = models.CharField(max_length=200, null=True, choices=TILA)
    työ = models.CharField(max_length=200, null=True, choices=TYÖ)
    luokka = models.CharField(max_length=200, null=True, choices=LUOKKA)
    järjestelmä = models.CharField(max_length=200, null=True, choices=JÄRJESTELMÄ)
    kuvaus = models.TextField(blank=True)
    listätieto = models.TextField(blank=True)
    laskutettu = models.CharField(max_length=200, default='Ei', choices=LASKUTETTU)

    class Meta:
        verbose_name_plural = "tilaukset"

    def __str__(self):
        return 'Tilausnumero #' + str(self.id)
    



class Työt(models.Model):
    lisännyt = CurrentUserField()
    tilausnumero = models.ForeignKey(Tilaus, null=True, on_delete=models.SET_NULL)
    päiväys = models.DateField(default=now)
    kuvaus = models.TextField(default='-')
    työnimi = models.CharField(max_length=50)
    työtuntia = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    työhinta = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    def __str__(self):
        return 'Työnumero ' + str(self.id)





class Tuote(models.Model):
    tilausnumero = models.ForeignKey(Tilaus, null=True, on_delete=models.SET_NULL)
    työnumero = models.ForeignKey(Työt, null=True, on_delete=models.SET_NULL)
    tuotetunnus = models.CharField(max_length=40, default='tunnus')
    tuotenimike = models.CharField(max_length=200, default='tuote')
    tuotemäärä = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    tuotehinta = models.DecimalField(max_digits=12, decimal_places=2, default=0)   

    class Meta:
        verbose_name_plural = "Lisää tuote"