"""
Motor de precios dinámico de TuVueloYa.

Algoritmo basado en el diagrama de datos del proyecto:
- Se calcula el promedio (mean) entre precio mínimo y máximo del vuelo.
- El precio final varía según el tipo de equipaje y qué tan cerca está
  el precio sugerido por el cliente del precio máximo (umbral: 85%).
"""


def calcular_precio(
    precio_minimo: float,
    precio_maximo: float,
    precio_sugerido: float,
    tipo_equipaje: str,
) -> float:
    """
    Calcula el precio final de un vuelo según las reglas de negocio.

    Equipaje de bodega (más pesado → más caro):
      - Si el cliente ofrece >= 85% del máximo → mean + 30%
      - Si ofrece menos                       → mean + 70%

    Equipaje de mano (más ligero → más barato):
      - Si el cliente ofrece >= 85% del máximo → mean - 30%
      - Si ofrece menos                       → mean - 70%
    """
    mean = (precio_maximo + precio_minimo) / 2
    umbral = 0.85 * precio_maximo

    if tipo_equipaje == "bodega":
        if precio_sugerido >= umbral:
            return round(mean * 1.3)
        return round(mean * 1.7)

    # tipo_equipaje == "mano"
    if precio_sugerido >= umbral:
        return round(mean * 0.7)
    return round(mean * 0.3)
