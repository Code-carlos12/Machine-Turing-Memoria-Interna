"""Modulo de cinta de la Maquina de Turing.

Representa la cinta infinita y las operaciones del cabezal:
lectura, escritura y movimiento en ambas direcciones.

La cinta se implementa como un diccionario {posicion: simbolo}
para permitir extension en ambas direcciones usando posiciones
negativas hacia la izquierda.

Reglas:
  - La posicion inicial del cabezal es 0 (primer caracter de la cadena).
  - La cinta contiene un blanco 'B' a la derecha de la entrada.
  - Si el cabezal se mueve fuera del rango conocido, se crea una celda 'B'.
  - No se elimina informacion escrita anteriormente.
"""

from __future__ import annotations

BLANCO = "B"


class Cinta:
    """Cinta de una Maquina de Turing con extension en ambas direcciones.

    Attributes:
        _celdas: Diccionario {posicion_entera: simbolo} con el contenido.
        _posicion: Posicion actual del cabezal.
    """

    def __init__(self, cadena: str) -> None:
        """Inicializa la cinta a partir de una cadena de entrada.

        Cada caracter se coloca en las posiciones 0, 1, 2, ...
        Se agrega un blanco 'B' inmediatamente despues del ultimo caracter.
        El cabezal se coloca en la posicion 0.

        Args:
            cadena: Cadena de entrada para la maquina. Puede estar vacia.
        """
        self._celdas: dict[int, str] = {}
        for i, caracter in enumerate(cadena):
            self._celdas[i] = caracter
        self._posicion: int = 0

    @property
    def posicion(self) -> int:
        """Posicion actual del cabezal."""
        return self._posicion

    def leer(self) -> str:
        """Lee el simbolo en la posicion actual del cabezal.

        Si la posicion no tiene una celda explicita, devuelve BLANCO ('B').
        """
        return self._celdas.get(self._posicion, BLANCO)

    def escribir(self, simbolo: str) -> None:
        """Escribe un simbolo en la posicion actual del cabezal.

        Args:
            simbolo: Simbolo a escribir en la celda actual (exactamente 1 caracter).

        Raises:
            ValueError: Si el simbolo no es exactamente un caracter.
        """
        if len(simbolo) != 1:
            raise ValueError(
                f"El simbolo debe ser exactamente un caracter, "
                f"se recibio: '{simbolo}' ({len(simbolo)} caracteres)."
            )
        self._celdas[self._posicion] = simbolo

    def mover_derecha(self) -> None:
        """Mueve el cabezal una posicion a la derecha."""
        self._posicion += 1

    def mover_izquierda(self) -> None:
        """Mueve el cabezal una posicion a la izquierda."""
        self._posicion -= 1

    def mover(self, direccion: str) -> None:
        """Mueve el cabezal en la direccion indicada ('L' o 'R')."""
        if direccion == "R":
            self.mover_derecha()
        elif direccion == "L":
            self.mover_izquierda()
        else:
            raise ValueError(
                f"Direccion invalida: '{direccion}'. Solo se permite 'L' o 'R'."
            )

    def obtener_contenido(self) -> dict[int, str]:
        """Devuelve una copia del contenido actual de la cinta."""
        return dict(self._celdas)

    def rango_posiciones(self) -> tuple[int, int]:
        """Devuelve el rango minimo y maximo de posiciones conocidas."""
        if not self._celdas:
            return (self._posicion, self._posicion)
        posiciones = list(self._celdas.keys()) + [self._posicion]
        return (min(posiciones), max(posiciones))

    def __repr__(self) -> str:
        r_min, r_max = self.rango_posiciones()
        celdas_str = "".join(self._celdas.get(i, BLANCO) for i in range(r_min, r_max + 1))
        return f"Cinta(pos={self._posicion}, celdas=[{r_min}:{r_max}]='{celdas_str}')"
