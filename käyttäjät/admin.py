from django.contrib import admin

from .models import *


class TyöKohdeAdmin(admin.ModelAdmin):
    search_fields = ['kohde']


class LaskutustiedotAdmin(admin.ModelAdmin):
    search_fields = ['yritys']


class AsiakasAdmin(admin.ModelAdmin):
    ordering = ['lisätty']
    search_fields = ['yritys']


class TilausAdmin(admin.ModelAdmin):
    autocomplete_fields = ['asiakas', 'työkohde', 'laskutustiedot']
    list_display = ('tila', 'työ', 'luokka', 'asiakas')
    search_fields = ['id']


    
   # def get_queryset(self, request):
    #    qs = super(TilausAdmin, self).get_queryset(request)
     #   return qs.exclude(tila='Valmis')
    


    

class TuoteInline(admin.TabularInline):
    autocomplete_fields = ['tilausnumero']
    model = Tuote
    extra = 1


    fieldsets = (
        (None, {
            'fields': ('tilausnumero', 'tuotetunnus', 'tuotenimike', 'tuotemäärä')

       
        }),
    )

    class Media:
        css = {
            'all': ('css/custom_admin.css', ) 
        }
    


class TuoteAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tilausnumero']



class TyötAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tilausnumero']
    model = Työt
    readonly_fields = ['lisännyt']
    inlines = [TuoteInline]
    

    class Media:
        css = {
            'all': ('css/custom_admin.css', ) 
        }
    
    

admin.site.register(Tuote, TuoteAdmin)
admin.site.register(Tilaus, TilausAdmin)
admin.site.register(Asiakas, AsiakasAdmin)
admin.site.register(TyöKohde, TyöKohdeAdmin)
admin.site.register(Työt, TyötAdmin)
admin.site.register(Laskutustiedot, LaskutustiedotAdmin)


