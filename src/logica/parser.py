"""Modulo de lectura del archivo de transiciones para MT con Memoria Interna.

Lee un archivo de texto con transiciones y produce:
  - Un diccionario indexado por (estado, simbolo_leido, memoria_origen) -> TransicionMemoria.
  - La lista de estados descubiertos.
  - La lista de simbolos descubiertos.
  - La lista de valores de memoria descubiertos.

Formato esperado de cada linea:
  estado_actual, simbolo_leido, memoria_actual -> estado_siguiente, simbolo_escrito, movimiento, memoria_siguiente

Se permiten:
  - Lineas vacias.
  - Comentarios con '#' (linea completa o al final de una transicion).
  - Espacios opcionales.
  - Notacion 'e', 'eps', 'epsilon' o 'ε' para la memoria vacia.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re

from logica.errores import ErrorArchivo, ErrorParser
from logica.transicion import TransicionMemoria, MEMORIA_VACIA


@dataclass
class ResultadoParser:
    """Resultado del analisis del archivo de transiciones con memoria.

    Attributes:
        transiciones: Diccionario {(estado, simbolo, memoria): TransicionMemoria}.
        estados: Lista ordenada de estados (q0 primero, qf ultimo).
        simbolos: Lista ordenada de simbolos (B ultimo).
        memorias: Lista ordenada de valores de memoria (ε primero).
        pares_estado_memoria: Lista ordenada de pares (estado, memoria).
    """

    transiciones: dict[tuple[str, str, str], TransicionMemoria] = field(default_factory=dict)
    estados: list[str] = field(default_factory=list)
    simbolos: list[str] = field(default_factory=list)
    memorias: list[str] = field(default_factory=list)
    pares_estado_memoria: list[tuple[str, str]] = field(default_factory=list)


def normalizar_memoria(valor: str) -> str:
    """Normaliza representaciones de memoria vacia ('e', 'eps', 'ε', etc.) a 'ε'."""
    v = valor.strip()
    if v.lower() in ("e", "eps", "epsilon", "vacio", "vacia", "none", "ε") or not v:
        return MEMORIA_VACIA
    return v


def parsear_archivo(ruta: str | Path) -> ResultadoParser:
    """Lee un archivo de transiciones con memoria interna y lo parsea.

    Args:
        ruta: Ruta al archivo de texto con las transiciones.

    Returns:
        ResultadoParser con la estructura procesada.

    Raises:
        ErrorArchivo: Si el archivo no existe o no se puede leer.
        ErrorParser: Si alguna linea presenta error sintactico.
    """
    ruta = Path(ruta)

    if not ruta.exists():
        raise ErrorArchivo(f"El archivo no existe: {ruta}")

    try:
        contenido = ruta.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise ErrorArchivo(f"No se puede leer el archivo: {ruta} ({e})")

    lineas = contenido.splitlines()

    transiciones: dict[tuple[str, str, str], TransicionMemoria] = {}
    estados_vistos: dict[str, None] = {}
    simbolos_vistos: dict[str, None] = {}
    memorias_vistas: dict[str, None] = {MEMORIA_VACIA: None}

    for num_linea, linea_cruda in enumerate(lineas, start=1):
        linea = linea_cruda.split("#")[0].strip()
        if not linea:
            continue

        transicion = _parsear_linea(linea, linea_cruda.strip(), num_linea)

        clave = transicion.clave_origen
        if clave in transiciones:
            raise ErrorParser(
                f"Transicion duplicada para el estado '{transicion.estado_origen}', "
                f"simbolo '{transicion.simbolo_leido}' y memoria '{transicion.memoria_origen}'.",
                linea=num_linea,
            )

        transiciones[clave] = transicion

        # Registrar apariciones
        for estado in (transicion.estado_origen, transicion.estado_destino):
            estados_vistos[estado] = None

        for simbolo in (transicion.simbolo_leido, transicion.simbolo_escrito):
            simbolos_vistos[simbolo] = None

        for mem in (transicion.memoria_origen, transicion.memoria_destino):
            memorias_vistas[mem] = None

    if "q0" not in estados_vistos:
        raise ErrorArchivo("Archivo Invalido: No se detecto el estado inicial 'q0' en las reglas.")
    if "qf" not in estados_vistos:
        raise ErrorArchivo("Archivo Invalido: No se detecto el estado de aceptacion 'qf' en las reglas.")

    estados = _ordenar_estados(list(estados_vistos.keys()))
    simbolos = _ordenar_simbolos(list(simbolos_vistos.keys()))
    memorias = _ordenar_memorias(list(memorias_vistas.keys()))

    # Construir pares ordenados (estado, memoria) alcanzables en el conjunto de reglas
    pares_vistos: dict[tuple[str, str], None] = {}
    for t in transiciones.values():
        pares_vistos[(t.estado_origen, t.memoria_origen)] = None
        pares_vistos[(t.estado_destino, t.memoria_destino)] = None

    if ("q0", MEMORIA_VACIA) not in pares_vistos:
        pares_vistos[("q0", MEMORIA_VACIA)] = None
    if ("qf", MEMORIA_VACIA) not in pares_vistos:
        pares_vistos[("qf", MEMORIA_VACIA)] = None

    pares_estado_memoria = sorted(
        list(pares_vistos.keys()),
        key=lambda p: (_clave_orden_estado(p[0]), _clave_orden_memoria(p[1]))
    )

    return ResultadoParser(
        transiciones=transiciones,
        estados=estados,
        simbolos=simbolos,
        memorias=memorias,
        pares_estado_memoria=pares_estado_memoria,
    )


def _parsear_linea(linea: str, linea_cruda: str, num_linea: int) -> TransicionMemoria:
    if "->" not in linea:
        raise ErrorParser(
            f"Falta el separador '->' en la transicion: '{linea_cruda}'",
            linea=num_linea,
        )

    partes = linea.split("->")
    if len(partes) != 2:
        raise ErrorParser(
            f"La linea contiene mas de un '->': '{linea_cruda}'",
            linea=num_linea,
        )

    lado_izq = partes[0].strip()
    lado_der = partes[1].strip()

    # Lado izquierdo: estado, simbolo, memoria
    campos_izq = [c.strip() for c in lado_izq.split(",")]
    if len(campos_izq) != 3:
        raise ErrorParser(
            f"Se esperan 3 campos antes de '->' (estado, simbolo, memoria). "
            f"Se encontraron {len(campos_izq)}: '{lado_izq}'",
            linea=num_linea,
        )
    estado_origen, simbolo_leido, memoria_origen = campos_izq
    memoria_origen = normalizar_memoria(memoria_origen)

    # Lado derecho: estado, simbolo, movimiento, memoria
    campos_der = [c.strip() for c in lado_der.split(",")]
    if len(campos_der) != 4:
        raise ErrorParser(
            f"Se esperan 4 campos despues de '->' (estado, simbolo, movimiento, memoria). "
            f"Se encontraron {len(campos_der)}: '{lado_der}'",
            linea=num_linea,
        )
    estado_destino, simbolo_escrito, movimiento, memoria_destino = campos_der
    memoria_destino = normalizar_memoria(memoria_destino)

    if movimiento not in ("L", "R"):
        raise ErrorParser(
            f"Movimiento invalido: '{movimiento}'. Solo se permite 'L' o 'R'.",
            linea=num_linea,
        )

    try:
        return TransicionMemoria(
            estado_origen=estado_origen,
            simbolo_leido=simbolo_leido,
            memoria_origen=memoria_origen,
            estado_destino=estado_destino,
            simbolo_escrito=simbolo_escrito,
            movimiento=movimiento,
            memoria_destino=memoria_destino,
        )
    except Exception as e:
        raise ErrorParser(str(e), linea=num_linea)


def _clave_orden_estado(estado: str) -> tuple:
    est = estado.lower()
    if est == "q0":
        return (0, 0, estado)
    if est in ("qf", "final", "qa", "qr"):
        return (2, 0, estado)
    match = re.search(r"\d+", estado)
    if match:
        return (1, int(match.group()), estado)
    return (1, 0, estado)


def _clave_orden_memoria(mem: str) -> tuple:
    if mem == MEMORIA_VACIA:
        return (0, mem)
    return (1, mem)


def _ordenar_estados(estados: list[str]) -> list[str]:
    return sorted(estados, key=_clave_orden_estado)


def _ordenar_simbolos(simbolos: list[str]) -> list[str]:
    def clave(s: str) -> tuple:
        if s == "B":
            return (3, s)
        if s.isdigit():
            return (0, int(s), s)
        if s in ("X", "Y"):
            return (2, s)
        return (1, s.lower(), s)

    return sorted(simbolos, key=clave)


def _ordenar_memorias(memorias: list[str]) -> list[str]:
    return sorted(memorias, key=_clave_orden_memoria)
