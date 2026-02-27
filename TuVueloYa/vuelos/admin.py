from django.contrib import admin

from .models import Reserva, Vuelo


@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ('numero', 'aerolinea', 'origen', 'destino', 'fecha', 'hora_salida', 'precio_minimo', 'precio_maximo')
    list_filter = ('aerolinea', 'origen', 'destino', 'fecha')
    search_fields = ('numero', 'origen', 'destino')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('codigo_reserva', 'nombre_pasajero', 'vuelo', 'tipo_equipaje', 'precio_final', 'metodo_pago')
    list_filter = ('tipo_equipaje', 'metodo_pago')
    search_fields = ('nombre_pasajero', 'codigo_reserva')
