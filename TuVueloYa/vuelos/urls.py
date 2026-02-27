from django.urls import path

from . import views

app_name = 'vuelos'

urlpatterns = [
    path('', views.index, name='index'),
    path('resultados/', views.resultados, name='resultados'),
    path('confirmar/<int:vuelo_id>/', views.confirmar, name='confirmar'),
    path('pago/<int:reserva_id>/', views.pago, name='pago'),
    path('boarding-pass/<int:reserva_id>/', views.boarding_pass, name='boarding_pass'),
]
