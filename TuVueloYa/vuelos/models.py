import uuid

from django.db import models


class Vuelo(models.Model):
    AEROLINEAS = [
        ('Avianca', 'Avianca'),
        ('Latam', 'Latam'),
        ('Viva Air', 'Viva Air'),
    ]
    CIUDADES = [
        ('Bogota', 'Bogotá'),
        ('Medellin', 'Medellín'),
        ('Cali', 'Cali'),
        ('Bucaramanga', 'Bucaramanga'),
        ('Cartagena', 'Cartagena'),
    ]

    numero = models.IntegerField(unique=True)
    aerolinea = models.CharField(max_length=32, choices=AEROLINEAS)
    origen = models.CharField(max_length=32, choices=CIUDADES)
    destino = models.CharField(max_length=32, choices=CIUDADES)
    fecha = models.DateField()
    hora_salida = models.TimeField()
    duracion = models.IntegerField(help_text="Duración en horas")
    precio_minimo = models.FloatField()
    precio_maximo = models.FloatField()

    class Meta:
        ordering = ['fecha', 'hora_salida']
        verbose_name_plural = 'Vuelos'

    def __str__(self) -> str:
        return f"Vuelo {self.numero} - {self.aerolinea}: {self.origen} → {self.destino}"


class Reserva(models.Model):
    EQUIPAJE_CHOICES = [
        ('mano', 'Equipaje de Mano'),
        ('bodega', 'Equipaje de Bodega'),
    ]
    PAGO_CHOICES = [
        ('credito', 'Tarjeta de Crédito'),
        ('debito', 'Tarjeta Débito'),
        ('pse', 'PSE'),
        ('efectivo', 'Efectivo'),
    ]

    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name='reservas')
    codigo_reserva = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre_pasajero = models.CharField(max_length=120)
    num_personas = models.IntegerField(default=1)
    tipo_equipaje = models.CharField(max_length=10, choices=EQUIPAJE_CHOICES)
    precio_sugerido = models.FloatField()
    precio_final = models.FloatField()
    metodo_pago = models.CharField(max_length=20, choices=PAGO_CHOICES, blank=True)
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_reserva']
        verbose_name_plural = 'Reservas'

    def __str__(self) -> str:
        return f"Reserva {self.codigo_reserva} - {self.nombre_pasajero}"
