from django.urls import path
from . import views

urlpatterns = [
    path('rekisteröidy/', views.rekisteröityminen, name="rekisteröidy"),
    path('kirjaudu/', views.kirjautuminen, name="kirjaudu"),
    path('kirjaudu_ulos/', views.kirjauduUlos, name="kirjaudu_ulos"),

    path('käyttäjä/', views.käyttäjäProfiili, name="käyttäjä_profiili"),

    path('käyttäjän_asetukset/', views.käyttäjänAsetukset, name="käyttäjän_asetukset"),

    path('', views.etusivu, name="etusivu"),

    path('asiakaslista/', views.asiakaslista, name="asiakaslista"),
    path('asiakas/<str:pk>', views.asiakkaat, name="asiakas"),

    path('arkisto/', views.arkisto, name="arkisto"),
    path('arkisto/<str:pk>', views.arkistoYksi, name="asiakasYksi"),


    path('työntekijälista/', views.työntekijälista, name="työntekijälista"),
    path('työkohteet/', views.työkohdelista, name="työkohdelista"),

    path('laskutustiedot/', views.laskutustietolista, name="laskutustietolista"),

    path('uusi_tilaus/', views.luoTilaus, name="uusi_tilaus"),
    path('päivitä_tilaus/<str:pk>', views.päivitäTilaus, name="päivitä_tilaus"),
    path('poista_tilaus/<str:pk>', views.poistaTilaus, name="poista_tilaus"),
]