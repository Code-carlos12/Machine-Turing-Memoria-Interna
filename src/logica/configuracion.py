"""Modelo de la configuracion instantanea de la Maquina de Turing con Memoria Interna.

Una configuracion es una fotografia inmutable de la maquina en un instante
determinado: paso, estado, memoria interna, cinta, posicion del cabezal,
simbolo leido y transicion aplicada/pendiente.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logica.transicion import TransicionMemoria


@dataclass(frozen=True, slots=True)
class Configuracion:
    """Fotografia inmutable de la maquina en un instante determinado.

    Attributes:
        paso: Numero de paso (0 = configuracion inicial).
        estado: Estado actual de la maquina.
        memoria: Valor actual de la memoria interna (ej. 'ε' o 'a').
        posicion_cabezal: Posicion entera del cabezal sobre la cinta.
        cinta: Vista de solo lectura del contenido de la cinta.
        simbolo_leido: Simbolo bajo el cabezal.
        transicion_aplicada: Transicion que condujo a este paso, o None en paso 0.
        transicion_pendiente: Transicion proxima a ejecutarse, o None si fin.
        motivo_detencion: Razon de parada (Aceptada, Rechazada, Detenida), o None.
        observacion: Breve descripcion de la operacion semantica realizada.
    """

    paso: int
    estado: str
    memoria: str
    posicion_cabezal: int
    cinta: MappingProxyType
    simbolo_leido: str
    transicion_aplicada: "TransicionMemoria | None" = field(default=None)
    transicion_pendiente: "TransicionMemoria | None" = field(default=None)
    motivo_detencion: str | None = field(default=None)
    observacion: str = field(default="")

    def __post_init__(self) -> None:
        if isinstance(self.cinta, dict):
            object.__setattr__(
                self, "cinta", MappingProxyType(dict(self.cinta))
            )

    def representacion_cinta_destacada(self) -> str:
        """Devuelve la cinta con la celda del cabezal entre corchetes.

        Ejemplo:
            [a]abb, X[a]bb, Xa[b]b, XXYY[B]
        """
        if not self.cinta:
            return f"[{self.simbolo_leido}]"

        indices = list(self.cinta.keys())
        min_idx = min(indices + [self.posicion_cabezal])
        max_idx = max(indices + [self.posicion_cabezal])

        # Recortar blancos superfluos a la izquierda y derecha que esten lejos del cabezal
        while min_idx < self.posicion_cabezal and self.cinta.get(min_idx, "B") == "B":
            min_idx += 1
        while max_idx > self.posicion_cabezal and self.cinta.get(max_idx, "B") == "B":
            max_idx -= 1

        partes = []
        for i in range(min_idx, max_idx + 1):
            val = self.cinta.get(i, "B")
            if i == self.posicion_cabezal:
                partes.append(f"[{val}]")
            else:
                partes.append(val)
        return "".join(partes)

    def id_formal(self) -> str:
        """Devuelve la descripcion instantanea formal en una linea.

        Ejemplo:
            X a [q1, a] b
        """
        if not self.cinta:
            return f"[{self.estado}, {self.memoria}] B"

        indices = list(self.cinta.keys())
        min_idx = min(indices + [self.posicion_cabezal])
        max_idx = max(indices + [self.posicion_cabezal])

        while min_idx < self.posicion_cabezal and self.cinta.get(min_idx, "B") == "B":
            min_idx += 1
        while max_idx > self.posicion_cabezal and self.cinta.get(max_idx, "B") == "B":
            max_idx -= 1

        partes = []
        for i in range(min_idx, max_idx + 1):
            if i == self.posicion_cabezal:
                partes.append(f"[{self.estado}, {self.memoria}]")
            partes.append(self.cinta.get(i, "B"))

        return " ".join(partes)
