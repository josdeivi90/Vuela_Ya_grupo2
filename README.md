# TuVueloYa - Sistema de Reserva de Vuelos Nacionales

Aplicación web para búsqueda y reserva de vuelos nacionales en Colombia, con motor de precios dinámico basado en el presupuesto del cliente y tipo de equipaje.

## Tecnologías

- **Backend**: Django 6.0 (Python)
- **Base de datos**: SQLite3
- **Frontend**: Bootstrap 5 + Bootstrap Icons (CDN)
- **QR**: qrcode[pil]

## Aerolíneas y ciudades

- **Aerolíneas**: Avianca, Latam, Viva Air
- **Ciudades**: Bogotá, Medellín, Cali, Bucaramanga, Cartagena
- **Datos**: 240 vuelos cargados desde CSV (diciembre 2021)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/josdeivi90/Vuela_Ya_grupo2.git
cd Vuela_Ya_grupo2

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
cd TuVueloYa
python manage.py migrate

# Cargar datos de vuelos desde CSV
python manage.py cargar_vuelos --archivo "../Cargar vuelos.csv"

# Crear usuario administrador (opcional)
python manage.py createsuperuser

# Iniciar el servidor
python manage.py runserver 8000
```

## Uso

| URL | Descripción |
|-----|-------------|
| http://127.0.0.1:8000/ | App principal - búsqueda y reserva de vuelos |
| http://127.0.0.1:8000/admin/ | Panel de administración - gestión de datos |

### Flujo de reserva

1. **Buscar**: seleccionar origen, destino, fecha, pasajeros, precio sugerido y tipo de equipaje.
2. **Resultados**: ver vuelos disponibles con precio dinámico calculado.
3. **Confirmar**: revisar detalle del vuelo e ingresar nombre del pasajero.
4. **Pagar**: seleccionar método de pago (crédito, débito, PSE, efectivo).
5. **Boarding pass**: recibir pase de abordar con código QR (imprimible).

### Fechas disponibles para pruebas

`2021-12-04`, `2021-12-05`, `2021-12-08`, `2021-12-11`, `2021-12-12`, `2021-12-18`, `2021-12-25`, `2021-12-26`

## Motor de precios

El precio final se calcula dinámicamente según el tipo de equipaje y el precio que sugiere el cliente:

```
mean = (precio_máximo + precio_mínimo) / 2

Equipaje de bodega:
  Si precio_sugerido >= 85% del máximo → precio_final = mean × 1.3
  Si no                                → precio_final = mean × 1.7

Equipaje de mano:
  Si precio_sugerido >= 85% del máximo → precio_final = mean × 0.7
  Si no                                → precio_final = mean × 0.3
```

## Estructura del proyecto

```
TuVueloYa/
├── TuVueloYa/              # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── vuelos/                  # App principal
│   ├── models.py            # Modelos Vuelo y Reserva
│   ├── views.py             # Vistas del flujo completo
│   ├── forms.py             # Formularios de búsqueda, confirmación y pago
│   ├── pricing.py           # Motor de precios dinámico
│   ├── urls.py              # Rutas de la app
│   ├── admin.py             # Configuración del panel admin
│   ├── management/commands/ # Comando cargar_vuelos (importar CSV)
│   └── templates/vuelos/    # Templates HTML
├── static/vuelos/css/       # Estilos personalizados
└── db.sqlite3               # Base de datos
```

## Equipo

Grupo 2 - Proyecto TuVueloYa
