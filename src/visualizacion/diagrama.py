"""Modulo para generar el diagrama de transiciones con Graphviz.

Visualiza los estados y las transiciones etiquetadas con los simbolos
de cinta, valores de memoria y desplazamientos del cabezal.
"""

from __future__ import annotations

import logging

try:
    import graphviz
    GRAPHVIZ_DISPONIBLE = True
except ImportError:
    graphviz = None
    GRAPHVIZ_DISPONIBLE = False

from logica.parser import ResultadoParser


class GeneradorDiagramaMemoria:
    """Construye el grafo de transiciones de la MT con Memoria Interna."""

    def __init__(self, parser_resultado: ResultadoParser) -> None:
        self.estados = parser_resultado.estados
        self.transiciones = parser_resultado.transiciones.values()

    def construir_grafo(self) -> "graphviz.Digraph | None":
        """Construye el objeto Digraph de Graphviz listo para renderizar."""
        if not GRAPHVIZ_DISPONIBLE or graphviz is None:
            logging.warning("Graphviz no esta disponible en el entorno.")
            return None

        dot = graphviz.Digraph(
            name="MT_Memoria_Interna",
            comment="Diagrama de Transiciones con Memoria Interna",
            format="png",
        )
        dot.attr(rankdir="LR")

        # 1. Configurar nodos
        for estado in self.estados:
            if estado == "qf":
                dot.node(estado, estado, shape="doublecircle")
            else:
                dot.node(estado, estado, shape="circle")

        # 2. Flecha de arranque en q0
        if "q0" in self.estados:
            dot.node("start", "", shape="none", width="0", height="0")
            dot.edge("start", "q0")

        # 3. Agrupar transiciones entre el mismo par (origen, destino)
        aristas: dict[tuple[str, str], list[str]] = {}
        for t in self.transiciones:
            clave = (t.estado_origen, t.estado_destino)
            if clave not in aristas:
                aristas[clave] = []
            aristas[clave].append(t.etiqueta_diagrama())

        # 4. Crear las aristas agregadas
        for (origen, destino), etiquetas in aristas.items():
            label = "\n".join(etiquetas)
            dot.edge(origen, destino, label=label)

        return dot
