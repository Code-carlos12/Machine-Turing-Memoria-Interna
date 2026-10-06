"""Jerarquia de excepciones del simulador de Maquina de Turing con Memoria Interna.

Todas las excepciones del simulador heredan de ErrorSimulador para que los
llamadores puedan capturar errores de forma generica o especifica.
"""


class ErrorSimulador(Exception):
    """Excepcion base para todos los errores del simulador."""


class ErrorParser(ErrorSimulador):
    """Se lanza cuando el archivo de transiciones contiene un error de sintaxis o formato.

    Attributes:
        linea: Numero de linea donde se encontro el error (1-indexado), o None.
    """

    def __init__(self, mensaje: str, linea: int | None = None) -> None:
        self.linea: int | None = linea
        prefijo = f"Linea {linea}: " if linea is not None else ""
        super().__init__(f"{prefijo}{mensaje}")


class ErrorTransicion(ErrorSimulador):
    """Se lanza cuando los datos de una Transicion son invalidos.

    Por ejemplo: movimiento distinto de 'L' o 'R', o campos vacios.
    """


class ErrorArchivo(ErrorSimulador):
    """Se lanza cuando el archivo de transiciones no puede abrirse o leerse."""
