"""Modelo de una transicion de la Maquina de Turing con Memoria Interna.

Representa de forma inmutable la tupla de transicion:
(estado_origen, simbolo_leido, memoria_origen) -> (estado_destino, simbolo_escrito, movimiento, memoria_destino)

La memoria interna finita permite condicionar la transicion tanto por el
simbolo bajo el cabezal como por el valor almacenado en la memoria interna,
y actualizar la memoria en cada paso.
"""

from __future__ import annotations

from dataclasses import dataclass
from logica.errores import ErrorTransicion

_MOVIMIENTOS_VALIDOS = frozenset({"L", "R"})
MEMORIA_VACIA = "ε"


@dataclass(frozen=True, slots=True)
class TransicionMemoria:
    """Transicion para una Maquina de Turing con Memoria Interna Finita.

    Attributes:
        estado_origen: Estado actual (q).
        simbolo_leido: Simbolo bajo el cabezal (s).
        memoria_origen: Valor actual de la memoria interna (m).
        estado_destino: Nuevo estado al que transita (q').
        simbolo_escrito: Simbolo a escribir en la cinta (s').
        movimiento: Direccion de movimiento del cabezal ('L' o 'R').
        memoria_destino: Nuevo valor de la memoria interna (m').
    """

    estado_origen: str
    simbolo_leido: str
    memoria_origen: str
    estado_destino: str
    simbolo_escrito: str
    movimiento: str
    memoria_destino: str

    def __post_init__(self) -> None:
        campos = {
            "estado_origen": self.estado_origen,
            "simbolo_leido": self.simbolo_leido,
            "memoria_origen": self.memoria_origen,
            "estado_destino": self.estado_destino,
            "simbolo_escrito": self.simbolo_escrito,
            "movimiento": self.movimiento,
            "memoria_destino": self.memoria_destino,
        }
        for nombre, valor in campos.items():
            if not valor or not valor.strip():
                raise ErrorTransicion(f"El campo '{nombre}' no puede estar vacio.")

        if len(self.simbolo_leido) != 1:
            raise ErrorTransicion(
                f"El simbolo leido debe ser exactamente un caracter, "
                f"se recibio: '{self.simbolo_leido}'."
            )
        if len(self.simbolo_escrito) != 1:
            raise ErrorTransicion(
                f"El simbolo escrito debe ser exactamente un caracter, "
                f"se recibio: '{self.simbolo_escrito}'."
            )

        if self.movimiento not in _MOVIMIENTOS_VALIDOS:
            raise ErrorTransicion(
                f"Movimiento invalido: '{self.movimiento}'. "
                f"Solo se permite 'L' (Izquierda) o 'R' (Derecha)."
            )

    @property
    def clave_origen(self) -> tuple[str, str, str]:
        """Clave de busqueda: (estado_origen, simbolo_leido, memoria_origen)."""
        return (self.estado_origen, self.simbolo_leido, self.memoria_origen)

    def etiqueta_diagrama(self) -> str:
        """Formato corto para la etiqueta de la arista en Graphviz."""
        return (
            f"{self.simbolo_leido}, {self.memoria_origen} / "
            f"{self.simbolo_escrito}, {self.movimiento}, {self.memoria_destino}"
        )

    def formato_accion(self) -> str:
        """Formato formal de accion utilizado en las tablas de simulacion."""
        return (
            f"{self.estado_origen},{self.simbolo_leido},{self.memoria_origen} = "
            f"{self.estado_destino},{self.simbolo_escrito},{self.movimiento},{self.memoria_destino}"
        )

    def __str__(self) -> str:
        return (
            f"{self.estado_origen}, {self.simbolo_leido}, {self.memoria_origen} -> "
            f"{self.estado_destino}, {self.simbolo_escrito}, {self.movimiento}, {self.memoria_destino}"
        )
