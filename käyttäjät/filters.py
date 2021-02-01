import django_filters
from django.db import models
from django.db.models import Q

from .models import *

class TilausFilter(django_filters.FilterSet):
    class Meta:
        model = Tilaus
        fields = ['tila', 'työkohde', 'tilauspäivä']


#class TilausHakuFilter(django_filters.FilterSet):
#    class Meta:
#        model = Tilaus
#        fields = ['kuvaus', 'listätieto']





class jono_TilausHakuFilter(django_filters.FilterSet):
    kuvaus = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = Tilaus
        fields = ['kuvaus']

    def my_custom_filter(self, queryset, name, value):
        return Tilaus.objects.filter(tila='Jonossa').filter(
            Q(kuvaus__icontains=value) | Q(listätieto__icontains=value) | Q(työ__icontains=value) |
             Q(asiakas__yritys__icontains=value) | Q(työkohde__osoite__icontains=value) | Q(työkohde__postinumero__icontains=value)
        )


class alla_TilausHakuFilter(django_filters.FilterSet):
    kuvaus = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = Tilaus
        fields = ['kuvaus']

    def my_custom_filter(self, queryset, name, value):
        return Tilaus.objects.filter(tila='Työn alla').filter(
            Q(kuvaus__icontains=value) | Q(listätieto__icontains=value) | Q(työ__icontains=value) | 
            Q(asiakas__yritys__icontains=value) | Q(työkohde__osoite__icontains=value) | Q(työkohde__postinumero__icontains=value)
        )


class valmis_TilausHakuFilter(django_filters.FilterSet):
    kuvaus = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = Tilaus
        fields = ['kuvaus']

    def my_custom_filter(self, queryset, name, value):
        return Tilaus.objects.filter(tila='Valmis').filter(
            Q(kuvaus__icontains=value) | Q(listätieto__icontains=value) | Q(työ__icontains=value) | 
            Q(asiakas__yritys__icontains=value) | Q(työkohde__osoite__icontains=value) | Q(työkohde__postinumero__icontains=value)
        )