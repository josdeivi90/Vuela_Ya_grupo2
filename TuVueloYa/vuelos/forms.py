from django import forms

from .models import Vuelo

CIUDADES = Vuelo.CIUDADES
EQUIPAJE = [
    ('mano', 'Equipaje de Mano'),
    ('bodega', 'Equipaje de Bodega'),
]


class BusquedaVueloForm(forms.Form):
    origen = forms.ChoiceField(
        choices=[('', 'Selecciona origen')] + CIUDADES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    destino = forms.ChoiceField(
        choices=[('', 'Selecciona destino')] + CIUDADES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    num_personas = forms.IntegerField(
        min_value=1,
        max_value=6,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Pasajeros',
    )
    precio_sugerido = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1500000',
        }),
        label='Precio sugerido (COP)',
    )
    tipo_equipaje = forms.ChoiceField(
        choices=EQUIPAJE,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo de equipaje',
    )


class ConfirmarReservaForm(forms.Form):
    nombre_pasajero = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo del pasajero',
        }),
        label='Nombre del pasajero',
    )


class PagoForm(forms.Form):
    METODOS = [
        ('credito', 'Tarjeta de Crédito'),
        ('debito', 'Tarjeta Débito'),
        ('pse', 'PSE'),
        ('efectivo', 'Efectivo'),
    ]
    metodo_pago = forms.ChoiceField(
        choices=METODOS,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Método de pago',
    )
