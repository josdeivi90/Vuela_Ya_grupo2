import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand

from vuelos.models import Vuelo


class Command(BaseCommand):
    help = 'Carga vuelos desde el archivo CSV "Cargar vuelos.csv"'

    def add_arguments(self, parser):
        default_path = Path(__file__).resolve().parents[4] / 'Cargar vuelos.csv'
        parser.add_argument(
            '--archivo',
            type=str,
            default=str(default_path),
            help='Ruta al archivo CSV de vuelos',
        )

    def handle(self, *args, **options):
        archivo = options['archivo']
        self.stdout.write(f"Cargando vuelos desde: {archivo}")

        creados = 0
        existentes = 0

        with open(archivo, encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                numero = int(row['Vuelo '].strip() if 'Vuelo ' in row else row['Vuelo'].strip())
                hora_str = row['Hora_Salida'].strip()
                hora = datetime.strptime(hora_str, '%H:%M').time()

                _, created = Vuelo.objects.get_or_create(
                    numero=numero,
                    defaults={
                        'aerolinea': row['Aerolinea'].strip(),
                        'origen': row['Origen'].strip(),
                        'destino': row['Destino'].strip(),
                        'fecha': row['Fecha'].strip(),
                        'hora_salida': hora,
                        'duracion': int(row['Duración'].strip()),
                        'precio_minimo': float(row['Precio_minimo'].strip()),
                        'precio_maximo': float(row['Precio_maximo'].strip()),
                    },
                )
                if created:
                    creados += 1
                else:
                    existentes += 1

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {creados} vuelos creados, {existentes} ya existían."
        ))
