from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import LuoKäyttäjäLomake, TilausLomake, AsiakasLomake
from .filters import *
from .decorators import unauthenticated_käyttäjä, allowed_käyttäjät, admin_only

from django.db.models import Sum



@unauthenticated_käyttäjä
def rekisteröityminen(request):

    lomake = LuoKäyttäjäLomake()

    if request.method == 'POST':
        lomake = LuoKäyttäjäLomake(request.POST)
        if lomake.is_valid():
            käyttäjä = lomake.save()
            käyttäjänimi = lomake.cleaned_data.get('username')
            group = Group.objects.get(name='asiakas')
            messages.success(request, 'Käyttäjä on luotu nimellä ' + käyttäjänimi)

            return redirect('kirjaudu')

    context = {'lomake':lomake}
    return render(request, 'käyttäjät/rekisteröidy.html', context)


@unauthenticated_käyttäjä
def kirjautuminen(request):
     
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        käyttäjä = authenticate(request, username=username, password=password)

        if käyttäjä is not None:
            login(request, käyttäjä)
            return redirect('etusivu')
        else:
            messages.info(request, 'Käyttäjänimi tai salasana on väärin')

    context = {}
    return render(request, 'käyttäjät/kirjaudu.html', context)


def kirjauduUlos(request):
    logout(request)
    return redirect('kirjaudu')

@login_required(login_url='kirjaudu')
@allowed_käyttäjät(allowed_roles=['asiakas'])
def käyttäjäProfiili(request):
    tilaukset = request.user.asiakas.tilaus_set.all()
    
    tilaukset_yht = tilaukset.count()
    valmiit_tilaukset = tilaukset.filter(tila='Valmis').count()
    jonossa_tilaukset = tilaukset.filter(tila='Jonossa').count()

    
    context = {'tilaukset':tilaukset, 'valmiit_tilaukset':valmiit_tilaukset, 'jonossa_tilaukset':jonossa_tilaukset, 'tilaukset_yht':tilaukset_yht}
    return render(request, 'käyttäjät/käyttäjä.html', context)


@login_required(login_url='kirjaudu')
@allowed_käyttäjät(allowed_roles=['asiakas'])
def käyttäjänAsetukset(request):
    asiakas = request.user.asiakas
    lomake = AsiakasLomake(instance=asiakas)

    if request.method == 'POST':
        lomake = AsiakasLomake(request.POST, request.FILES, instance=asiakas)
        if lomake.is_valid():
            lomake.save()

    context = {'lomake':lomake}
    return render(request, 'käyttäjät/käyttäjän_asetukset.html', context)





@login_required(login_url='kirjaudu')
@admin_only
def etusivu(request):


    

    työt = Työt.objects.all()
    tilaukset = Tilaus.objects.all()
    
    asiakkaat = Asiakas.objects.all()
    työnkohteet = TyöKohde.objects.all()
    ei_valmiit_tilaukset = tilaukset.exclude(tila='Valmis')
    valmiit_tilaukset = tilaukset.filter(tila='Valmis')
    asiakkaat_yht = asiakkaat.count()
    tilaukset_yht = tilaukset.count()
    valmiit_tilaukset = tilaukset.filter(tila='Valmis').count()
    jonossa_tilaukset = tilaukset.filter(tila='Jonossa').count()
    
    from datetime import date
    tp = date.today()

    #Jonossa
    jono_tilaukset = Tilaus.objects.all().filter(tila='Jonossa').exclude(laskutettu='Kyllä')
    jono_tilausFilter = jono_TilausHakuFilter(request.GET, queryset=jono_tilaukset)
    jono_tilaukset = jono_tilausFilter.qs

    #Työn alla   
    alla_tilaukset = Tilaus.objects.all().filter(tila='Työn alla').exclude(laskutettu='Kyllä')
    alla_tilausFilter = alla_TilausHakuFilter(request.GET, queryset=alla_tilaukset)
    alla_tilaukset = alla_tilausFilter.qs




    #valmis
    tilaukset = Tilaus.objects.all().filter(tila='Valmis').exclude(laskutettu='Kyllä')
    tilausFilter = valmis_TilausHakuFilter(request.GET, queryset=tilaukset)
    tilaukset = tilausFilter.qs

    

    context = {'tilaukset':tilaukset, 'asiakkaat':asiakkaat, 'työnkohteet':työnkohteet,
    'asiakkaat_yht':asiakkaat_yht, 'tilaukset_yht':tilaukset_yht, 'valmiit_tilaukset':valmiit_tilaukset,
    'jonossa_tilaukset':jonossa_tilaukset, 'ei_valmiit_tilaukset':ei_valmiit_tilaukset,
    'tilausFilter':tilausFilter, 'jono_tilausFilter':jono_tilausFilter, 'jono_tilaukset':jono_tilaukset, 
    'alla_tilaukset':alla_tilaukset, 'alla_tilausFilter':alla_tilausFilter, 'tp':tp, 'työt':työt,
    
   
    }

    return render(request, 'käyttäjät/dashboard.html', context)





@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def asiakkaat(request, pk):
    asiakas = Asiakas.objects.get(id=pk)
    tilaukset = asiakas.tilaus_set.all()
    tilaukset_yht = tilaukset.count()

    asiakasFilter = TilausFilter(request.GET, queryset=tilaukset)
    tilaukset = asiakasFilter.qs

    context = {'asiakas':asiakas, 'tilaukset':tilaukset, 'tilaukset_yht':tilaukset_yht, 'asiakasFilter':asiakasFilter}
    return render(request, 'käyttäjät/asiakas.html', context)


@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def asiakaslista(request):
    asiakkaat = Asiakas.objects.all()
    context = {'asiakkaat':asiakkaat}

    return render(request, 'käyttäjät/asiakaslista.html', context)


@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def arkisto(request):
    tilaukset = Tilaus.objects.all()
    laskutetut_tilaukset = tilaukset.filter(laskutettu='Kyllä')
    context = {'laskutetut_tilaukset':laskutetut_tilaukset, 'tilaukset':tilaukset}
    return render(request, 'käyttäjät/arkisto.html', context)


@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def arkistoYksi(request, pk):
    tilaukset = Tilaus.objects.get(id=pk)
    työt = Työt.objects.filter(tilausnumero=pk)
    tuoteyksi = Tuote.objects.filter(tilausnumero=pk)
    


    context = {'tilaukset':tilaukset, 'työt':työt, 'tuoteyksi':tuoteyksi}
    return render(request, 'käyttäjät/arkistoYksi.html', context)


@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def työntekijälista(request):
    users = User.objects.all()

    context = {'users':users}

    return render(request, 'käyttäjät/työntekijälista.html', context)


@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def työkohdelista(request):
    työkohteet = TyöKohde.objects.all()
    context = {'työkohteet':työkohteet}

    return render(request, 'käyttäjät/työkohdelista.html', context)


@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def laskutustietolista(request):
    laskutustiedot = Laskutustiedot.objects.all()
    context = {'laskutustiedot':laskutustiedot}

    return render(request, 'käyttäjät/laskutustietolista.html', context)


@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def luoTilaus(request):

    lomake = TilausLomake()
    if request.method == 'POST':
        lomake = TilausLomake(request.POST)
        if lomake.is_valid():
            lomake.save()
            return redirect('/')
    
    context = {'lomake':lomake}
    return render(request, 'käyttäjät/uusi_tilaus.html', context)


@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def päivitäTilaus(request, pk):

    tilaus = Tilaus.objects.get(id=pk)
    lomake = TilausLomake(instance=tilaus)

    if request.method == 'POST':
        lomake = TilausLomake(request.POST, instance=tilaus)
        if lomake.is_valid():
            lomake.save()
            return redirect('/')

    context = {'lomake':lomake, 'tilaus':tilaus}
    return render(request, 'käyttäjät/uusi_tilaus.html', context)


@allowed_käyttäjät(allowed_roles=['admin'])
@login_required(login_url='kirjaudu')
def poistaTilaus(request, pk):
    tilaus = Tilaus.objects.get(id=pk)
    if request.method == "POST":
        tilaus.delete()
        return redirect('/')
    context = {'item':tilaus}
    return render(request, 'käyttäjät/poista.html', context)