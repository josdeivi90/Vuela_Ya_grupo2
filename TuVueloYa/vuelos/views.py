import base64
import io
from typing import Any

import qrcode
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BusquedaVueloForm, ConfirmarReservaForm, PagoForm
from .models import Reserva, Vuelo
from .pricing import calcular_precio


def index(request: HttpRequest) -> HttpResponse:
    """Página de inicio con el formulario de búsqueda de vuelos."""
    form = BusquedaVueloForm()
    return render(request, 'vuelos/index.html', {'form': form})


def resultados(request: HttpRequest) -> HttpResponse:
    """Busca vuelos y calcula precios dinámicos para cada resultado."""
    form = BusquedaVueloForm(request.GET)
    if not form.is_valid():
        return render(request, 'vuelos/index.html', {'form': form})

    datos = form.cleaned_data
    vuelos_qs = Vuelo.objects.filter(
        origen=datos['origen'],
        destino=datos['destino'],
        fecha=datos['fecha'],
    )

    resultados_list: list[dict[str, Any]] = []
    for vuelo in vuelos_qs:
        precio = calcular_precio(
            vuelo.precio_minimo,
            vuelo.precio_maximo,
            datos['precio_sugerido'],
            datos['tipo_equipaje'],
        )
        precio_total = precio * datos['num_personas']
        resultados_list.append({
            'vuelo': vuelo,
            'precio_unitario': precio,
            'precio_total': precio_total,
        })

    context = {
        'resultados': resultados_list,
        'datos': datos,
        'form': form,
    }
    return render(request, 'vuelos/resultados.html', context)


def confirmar(request: HttpRequest, vuelo_id: int) -> HttpResponse:
    """Muestra resumen del vuelo y pide datos del pasajero para confirmar."""
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)

    precio_sugerido = float(request.GET.get('precio_sugerido', 0))
    tipo_equipaje = request.GET.get('tipo_equipaje', 'mano')
    num_personas = int(request.GET.get('num_personas', 1))

    precio_unitario = calcular_precio(
        vuelo.precio_minimo,
        vuelo.precio_maximo,
        precio_sugerido,
        tipo_equipaje,
    )
    precio_total = precio_unitario * num_personas

    if request.method == 'POST':
        form = ConfirmarReservaForm(request.POST)
        if form.is_valid():
            reserva = Reserva.objects.create(
                vuelo=vuelo,
                nombre_pasajero=form.cleaned_data['nombre_pasajero'],
                num_personas=num_personas,
                tipo_equipaje=tipo_equipaje,
                precio_sugerido=precio_sugerido,
                precio_final=precio_total,
            )
            return redirect('vuelos:pago', reserva_id=reserva.pk)
    else:
        form = ConfirmarReservaForm()

    context = {
        'vuelo': vuelo,
        'form': form,
        'precio_unitario': precio_unitario,
        'precio_total': precio_total,
        'num_personas': num_personas,
        'tipo_equipaje': tipo_equipaje,
        'precio_sugerido': precio_sugerido,
    }
    return render(request, 'vuelos/confirmar.html', context)


def pago(request: HttpRequest, reserva_id: int) -> HttpResponse:
    """Selección de método de pago para la reserva."""
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            reserva.metodo_pago = form.cleaned_data['metodo_pago']
            reserva.save()
            return redirect('vuelos:boarding_pass', reserva_id=reserva.pk)
    else:
        form = PagoForm()

    return render(request, 'vuelos/pago.html', {'reserva': reserva, 'form': form})


def boarding_pass(request: HttpRequest, reserva_id: int) -> HttpResponse:
    """Genera y muestra el boarding pass con código QR."""
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    qr_data = (
        f"TuVueloYa | Reserva: {reserva.codigo_reserva}\n"
        f"Pasajero: {reserva.nombre_pasajero}\n"
        f"Vuelo: {reserva.vuelo.numero} - {reserva.vuelo.aerolinea}\n"
        f"Ruta: {reserva.vuelo.origen} → {reserva.vuelo.destino}\n"
        f"Fecha: {reserva.vuelo.fecha} | Hora: {reserva.vuelo.hora_salida}\n"
        f"Total: ${reserva.precio_final:,.0f} COP"
    )
    img = qrcode.make(qr_data)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'reserva': reserva,
        'qr_image': qr_base64,
    }
    return render(request, 'vuelos/boarding_pass.html', context)
