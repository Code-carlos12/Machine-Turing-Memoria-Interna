"""Motor de ejecucion de la Maquina de Turing con Memoria Interna Finita.

Controla el ciclo de ejecucion, administra la cinta, el estado actual,
el contenido de la memoria interna y genera el historial de configuraciones
instantaneas.
"""

from __future__ import annotations

from logica.cinta import Cinta
from logica.configuracion import Configuracion
from logica.transicion import TransicionMemoria, MEMORIA_VACIA


class MaquinaTuringMemoria:
    """Simulador de Maquina de Turing con memoria interna finita."""

    ESTADO_INICIAL = "q0"
    ESTADO_FINAL = "qf"
    MEMORIA_INICIAL = MEMORIA_VACIA

    RESULTADO_ACEPTADA = "CADENA ACEPTADA"
    RESULTADO_RECHAZADA = "CADENA RECHAZADA"
    RESULTADO_DETENIDA = "EJECUCION DETENIDA POR EL USUARIO"

    def __init__(self, transiciones: dict[tuple[str, str, str], TransicionMemoria]) -> None:
        """Inicializa el motor con el mapa de transiciones.

        Args:
            transiciones: Diccionario indexado por (estado, simbolo_leido, memoria).
        """
        self.transiciones = transiciones
        self.cinta: Cinta | None = None
        self.estado_actual: str = ""
        self.memoria_actual: str = self.MEMORIA_INICIAL
        self.paso_actual: int = 0
        self.estado_ejecucion: str = "NO_INICIADA"
        self.ultima_transicion: TransicionMemoria | None = None
        self.historial: list[Configuracion] = []

    def iniciar(self, cadena: str) -> None:
        """Inicializa la maquina para evaluar una cadena dada."""
        self.cinta = Cinta(cadena)
        self.estado_actual = self.ESTADO_INICIAL
        self.memoria_actual = self.MEMORIA_INICIAL
        self.paso_actual = 0
        self.estado_ejecucion = "EN_CURSO"
        self.ultima_transicion = None
        self.historial = []

        # Registro del Paso 0 (configuracion inicial)
        self._registrar_configuracion()

    def paso(self) -> bool:
        """Ejecuta exactamente un paso de transicion.

        Returns:
            True si la maquina permanece EN_CURSO; False si llego a un estado terminal.
        """
        if self.estado_ejecucion != "EN_CURSO" or self.cinta is None:
            return False

        simbolo = self.cinta.leer()
        clave = (self.estado_actual, simbolo, self.memoria_actual)
        transicion = self.transiciones.get(clave)

        if not transicion:
            self.estado_ejecucion = "RECHAZADA"
            return False

        # 1. Escribir en cinta
        self.cinta.escribir(transicion.simbolo_escrito)
        # 2. Mover el cabezal
        self.cinta.mover(transicion.movimiento)
        # 3. Transicion de estado de control
        self.estado_actual = transicion.estado_destino
        # 4. Actualizacion de la memoria interna
        self.memoria_actual = transicion.memoria_destino
        # 5. Actualizar contadores y ultima transicion
        self.paso_actual += 1
        self.ultima_transicion = transicion

        # 6. Registrar configuracion resultante
        self._registrar_configuracion()

        return self.estado_ejecucion == "EN_CURSO"

    def ejecutar_todo(self) -> None:
        """Ejecuta pasos consecutivamente hasta llegar a un estado final o rechazo."""
        while self.estado_ejecucion == "EN_CURSO":
            self.paso()

    def detener(self) -> None:
        """Detiene manualmente una ejecucion en curso."""
        if self.estado_ejecucion == "EN_CURSO":
            self.estado_ejecucion = "DETENIDA"
            if self.historial:
                ultima = self.historial.pop()
                cfg_detenida = Configuracion(
                    paso=ultima.paso,
                    estado=ultima.estado,
                    memoria=ultima.memoria,
                    posicion_cabezal=ultima.posicion_cabezal,
                    cinta=ultima.cinta,
                    simbolo_leido=ultima.simbolo_leido,
                    transicion_aplicada=ultima.transicion_aplicada,
                    transicion_pendiente=None,
                    motivo_detencion=self.RESULTADO_DETENIDA,
                )
                self.historial.append(cfg_detenida)

    def _registrar_configuracion(self) -> None:
        if self.cinta is None:
            return

        simbolo = self.cinta.leer()
        clave = (self.estado_actual, simbolo, self.memoria_actual)
        pendiente = self.transiciones.get(clave)
        motivo = None

        if self.estado_ejecucion == "DETENIDA":
            motivo = self.RESULTADO_DETENIDA
            pendiente = None
        elif self.estado_actual == self.ESTADO_FINAL:
            # Si alcanza qf y la memoria esta vacia, acepta
            if self.memoria_actual == self.MEMORIA_INICIAL:
                self.estado_ejecucion = "ACEPTADA"
                motivo = self.RESULTADO_ACEPTADA
            else:
                self.estado_ejecucion = "RECHAZADA"
                motivo = f"Estado final alcanzado pero memoria no vacia (m = {self.memoria_actual})."
            pendiente = None
        elif not pendiente:
            self.estado_ejecucion = "RECHAZADA"
            motivo = (
                f"No existe transicion para estado '{self.estado_actual}', "
                f"simbolo '{simbolo}' y memoria '{self.memoria_actual}'."
            )

        cfg = Configuracion(
            paso=self.paso_actual,
            estado=self.estado_actual,
            memoria=self.memoria_actual,
            posicion_cabezal=self.cinta.posicion,
            cinta=self.cinta.obtener_contenido(),
            simbolo_leido=simbolo,
            transicion_aplicada=self.ultima_transicion,
            transicion_pendiente=pendiente,
            motivo_detencion=motivo,
        )
        self.historial.append(cfg)
