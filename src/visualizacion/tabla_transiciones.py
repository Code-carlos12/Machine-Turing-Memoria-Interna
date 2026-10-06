"""Modulo para generar la tabla de transiciones matricial con memoria interna.

Transforma las transiciones en una matriz donde las filas representan
los estados combinados con la memoria interna (q, m) y las columnas
representan los simbolos de cinta.

No contiene dependencias directas de GUI.
"""

from __future__ import annotations

from logica.parser import ResultadoParser


class GeneradorTablaMemoria:
    """Prepara los datos matriciales para la visualizacion de la tabla."""

    def __init__(self, parser_resultado: ResultadoParser) -> None:
        self.transiciones = parser_resultado.transiciones
        self.simbolos = list(parser_resultado.simbolos)
        self.pares_estado_memoria = list(parser_resultado.pares_estado_memoria)

    def obtener_columnas(self) -> list[str]:
        """Encabezados: 'Estado (q, m)' seguido de los simbolos de cinta."""
        return ["(q, m)"] + self.simbolos

    def obtener_filas(self) -> list[list[str]]:
        """Genera las filas matriciales de transiciones."""
        filas = []
        for estado, mem in self.pares_estado_memoria:
            etiqueta_fila = f"({estado}, {mem})"
            fila = [etiqueta_fila]

            for simbolo in self.simbolos:
                clave = (estado, simbolo, mem)
                t = self.transiciones.get(clave)
                if t is not None:
                    celda = f"{t.estado_destino}, {t.simbolo_escrito}, {t.movimiento}, {t.memoria_destino}"
                else:
                    celda = "-"
                fila.append(celda)

            filas.append(fila)

        return filas
