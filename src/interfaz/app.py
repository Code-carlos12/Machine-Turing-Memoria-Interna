"""Interfaz grafica principal del Simulador de Maquina de Turing con Memoria Interna."""

from __future__ import annotations

import os
import time
import tempfile
import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Solucionar escalado borroso en pantallas de alta densidad (DPI)
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

try:
    import graphviz
    from graphviz.backend.execute import ExecutableNotFound
except ImportError:
    graphviz = None
    ExecutableNotFound = Exception

from logica.parser import parsear_archivo, ResultadoParser
from logica.errores import ErrorArchivo, ErrorParser
from logica.maquina_turing import MaquinaTuringMemoria
from logica.configuracion import Configuracion
from logica.transicion import MEMORIA_VACIA
from visualizacion.tabla_transiciones import GeneradorTablaMemoria
from visualizacion.diagrama import GeneradorDiagramaMemoria


class SimuladorMemoriaApp:
    """Ventana y controlador de la interfaz de usuario del simulador."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Simulador de Máquina de Turing con Memoria Interna Finita")
        self.root.geometry("1280x850")

        # Maximizar ventana dinamicamente
        try:
            self.root.state("zoomed")
        except tk.TclError:
            try:
                self.root.attributes("-zoomed", True)
            except tk.TclError:
                w = self.root.winfo_screenwidth()
                h = self.root.winfo_screenheight()
                self.root.geometry(f"{w}x{h}+0+0")

        self._configurar_estilos()

        # Estado de la aplicacion
        self.resultado_parser: ResultadoParser | None = None
        self.motor: MaquinaTuringMemoria | None = None
        self._img_diagrama = None
        self.nombre_archivo_actual: str | None = None

        # Concurrencia y sincronizacion
        self.hilo_ejecucion: threading.Thread | None = None
        self.evento_detener = threading.Event()
        self.cola_actualizaciones: queue.Queue[str] = queue.Queue()
        self.ultimo_paso_mostrado = -1

        self._construir_menu()
        self._construir_ui()

    def _configurar_estilos(self) -> None:
        style = ttk.Style()
        style.configure("Treeview", font=("Consolas", 10), rowheight=26)
        style.configure("Treeview.Heading", font=("Consolas", 10, "bold"))

    def _construir_menu(self) -> None:
        menubar = tk.Menu(self.root)

        menu_pref = tk.Menu(menubar, tearoff=0)
        self.var_velocidad = tk.StringVar(value="Media")

        menu_velocidad = tk.Menu(menu_pref, tearoff=0)
        menu_velocidad.add_radiobutton(label="Lenta (1.0s)", variable=self.var_velocidad, value="Lenta")
        menu_velocidad.add_radiobutton(label="Media (0.5s)", variable=self.var_velocidad, value="Media")
        menu_velocidad.add_radiobutton(label="Rapida (0.1s)", variable=self.var_velocidad, value="Rapida")
        menu_velocidad.add_radiobutton(label="Inmediata (Sin retardo)", variable=self.var_velocidad, value="Inmediata")

        menu_pref.add_cascade(label="Velocidad de simulacion", menu=menu_velocidad)
        menubar.add_cascade(label="Preferencias", menu=menu_pref)

        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menu_ayuda.add_command(label="Manual de uso y formato", command=self._mostrar_manual)
        menu_ayuda.add_separator()
        menu_ayuda.add_command(label="Acerca del simulador", command=self._mostrar_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.root.config(menu=menubar)

    def _mostrar_manual(self) -> None:
        info = (
            "MANUAL DE USUARIO - MT CON MEMORIA INTERNA FINITA\n\n"
            "Este simulador procesa reglas para Máquinas de Turing con memoria interna.\n\n"
            "FORMATO ESTRICTO POR LINEA:\n"
            "estado_actual, simbolo_leido, memoria_actual -> "
            "estado_sig, simbolo_escrito, movimiento, memoria_sig\n\n"
            "REGLAS:\n"
            "1. Estados: El estado inicial obligatorio es 'q0' y el de aceptacion es 'qf'.\n"
            "2. Memoria Vacia: Puede escribirse como 'e', 'eps' o 'ε'.\n"
            "3. Movimiento: 'R' (Derecha) o 'L' (Izquierda).\n"
            "4. Simbolo Blanco: Representado exclusivamente por 'B'.\n"
            "5. Comentarios: Se admiten anotaciones con el caracter '#'.\n\n"
            "EJEMPLO:\n"
            "q0, a, e -> q1, X, R, a\n"
            "q1, b, a -> q1, Y, L, e"
        )
        messagebox.showinfo("Manual de uso", info)

    def _mostrar_acerca_de(self) -> None:
        info = (
            "Universidad de Panamá\n"
            "Facultad de Informática, Electrónica y Comunicación\n"
            "Ingeniería en Informática\n\n"
            "Simulador de Máquina de Turing con Memoria Interna Finita\n"
            "Reconocedor para L = { a^n b^n | n >= 1 }\n"
            "Año: 2026"
        )
        messagebox.showinfo("Acerca del simulador", info)

    def _construir_ui(self) -> None:
        # 1. Barra de Controles Superior
        frame_controles = ttk.LabelFrame(self.root, text="Controles de ejecucion", padding=10)
        frame_controles.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_controles, text="Cargar archivo (.txt)", command=self._cargar_archivo).pack(side=tk.LEFT, padx=5)
        self.lbl_archivo = ttk.Label(frame_controles, text="Sin archivo cargado", foreground="gray")
        self.lbl_archivo.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_controles, text="Cadena de entrada:").pack(side=tk.LEFT, padx=(20, 5))
        self.var_cadena = tk.StringVar(value="aabb")
        self.var_cadena.trace_add("write", self._actualizar_cinta_previa)
        self.entry_cadena = ttk.Entry(frame_controles, textvariable=self.var_cadena, width=22)
        self.entry_cadena.pack(side=tk.LEFT, padx=5)

        self.btn_iniciar = ttk.Button(frame_controles, text="Iniciar Automatica", command=self._iniciar_maquina, state=tk.DISABLED)
        self.btn_iniciar.pack(side=tk.LEFT, padx=8)

        self.btn_paso = ttk.Button(frame_controles, text="Paso Manual", command=self._paso_a_paso, state=tk.DISABLED)
        self.btn_paso.pack(side=tk.LEFT, padx=5)

        self.btn_stop = ttk.Button(frame_controles, text="Detener", command=self._detener, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.lbl_estado = ttk.Label(frame_controles, text="NO INICIADA", font=("Arial", 11, "bold"))
        self.lbl_estado.pack(side=tk.RIGHT, padx=10)

        # 2. Cuadricula Principal 2x2
        self.panel_principal = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.panel_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Fila 1 (Superior)
        self.panel_fila1 = ttk.PanedWindow(self.panel_principal, orient=tk.HORIZONTAL)
        self.panel_principal.add(self.panel_fila1, weight=1)

        # [1, 1] Tabla de Transiciones (Matriz)
        frame_tabla = ttk.LabelFrame(self.panel_fila1, text="Tabla de Transiciones δ : (q, m) × Γ")
        self.panel_fila1.add(frame_tabla, weight=1)
        self.canvas_tabla = tk.Canvas(frame_tabla, bg="white", highlightthickness=0)
        scroll_t_y = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.canvas_tabla.yview)
        scroll_t_x = ttk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL, command=self.canvas_tabla.xview)
        self.canvas_tabla.configure(yscrollcommand=scroll_t_y.set, xscrollcommand=scroll_t_x.set)
        scroll_t_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_t_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas_tabla.pack(fill=tk.BOTH, expand=True)

        # [1, 2] Diagrama de Transiciones (Grafo)
        frame_diagrama = ttk.LabelFrame(self.panel_fila1, text="Diagrama de Estados (Graphviz)")
        self.panel_fila1.add(frame_diagrama, weight=1)
        self.canvas_diagrama = tk.Canvas(frame_diagrama, bg="white")
        scroll_d_y = ttk.Scrollbar(frame_diagrama, orient=tk.VERTICAL, command=self.canvas_diagrama.yview)
        scroll_d_x = ttk.Scrollbar(frame_diagrama, orient=tk.HORIZONTAL, command=self.canvas_diagrama.xview)
        self.canvas_diagrama.configure(yscrollcommand=scroll_d_y.set, xscrollcommand=scroll_d_x.set)
        scroll_d_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_d_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas_diagrama.pack(fill=tk.BOTH, expand=True)
        self.lbl_diagrama_fallback = ttk.Label(self.canvas_diagrama, text="Cargue un archivo para generar el grafo.")
        self.lbl_diagrama_fallback.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Fila 2 (Inferior)
        self.panel_fila2 = ttk.PanedWindow(self.panel_principal, orient=tk.HORIZONTAL)
        self.panel_principal.add(self.panel_fila2, weight=1)

        # [2, 1] Cinta Visual Interactiva
        frame_cinta = ttk.LabelFrame(self.panel_fila2, text="Cinta Visual y Memoria Interna")
        self.panel_fila2.add(frame_cinta, weight=1)
        self.canvas_cinta = tk.Canvas(frame_cinta, bg="white")
        scroll_c_y = ttk.Scrollbar(frame_cinta, orient=tk.VERTICAL, command=self.canvas_cinta.yview)
        scroll_c_x = ttk.Scrollbar(frame_cinta, orient=tk.HORIZONTAL, command=self.canvas_cinta.xview)
        self.canvas_cinta.configure(yscrollcommand=scroll_c_y.set, xscrollcommand=scroll_c_x.set)
        scroll_c_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_c_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas_cinta.pack(fill=tk.BOTH, expand=True)

        # [2, 2] Historial de Descripciones Instantaneas
        frame_historial = ttk.LabelFrame(self.panel_fila2, text="Historial de Descripciones Instantaneas y Acciones")
        self.panel_fila2.add(frame_historial, weight=1)

        columnas_hist = ("Paso", "Estado", "Memoria", "Cinta", "Accion")
        self.tree_historial = ttk.Treeview(frame_historial, columns=columnas_hist, show="headings")

        self.tree_historial.heading("Paso", text="Paso")
        self.tree_historial.heading("Estado", text="Estado")
        self.tree_historial.heading("Memoria", text="Memoria")
        self.tree_historial.heading("Cinta", text="Cinta")
        self.tree_historial.heading("Accion", text="Accion")

        self.tree_historial.column("Paso", width=60, anchor=tk.CENTER, stretch=False)
        self.tree_historial.column("Estado", width=75, anchor=tk.CENTER, stretch=False)
        self.tree_historial.column("Memoria", width=80, anchor=tk.CENTER, stretch=False)
        self.tree_historial.column("Cinta", width=140, anchor=tk.W, stretch=False)
        self.tree_historial.column("Accion", width=300, anchor=tk.W, stretch=True)

        scroll_h_y = ttk.Scrollbar(frame_historial, orient=tk.VERTICAL, command=self.tree_historial.yview)
        self.tree_historial.configure(yscrollcommand=scroll_h_y.set)

        # Barra inferior de resultados y exportacion
        frame_bottom_hist = ttk.Frame(frame_historial)
        frame_bottom_hist.pack(side=tk.BOTTOM, fill=tk.X, pady=5, padx=5)

        self.lbl_solucion = ttk.Label(frame_bottom_hist, text="", font=("Consolas", 12, "bold"))
        self.lbl_solucion.pack(side=tk.LEFT)

        self.btn_exportar = ttk.Button(
            frame_bottom_hist,
            text="Guardar Historial (.txt)",
            command=self._exportar_historial,
            state=tk.DISABLED,
        )
        self.btn_exportar.pack(side=tk.RIGHT)

        scroll_h_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_historial.pack(fill=tk.BOTH, expand=True)

        self.tree_historial.tag_configure("fila_par", background="#F0F8FF")
        self.tree_historial.tag_configure("fila_impar", background="#FFFFFF")

    def _actualizar_cinta_previa(self, *args) -> None:
        if self.motor and self.motor.estado_ejecucion in ["EN_CURSO", "DETENIDA"]:
            return

        if self.motor and self.motor.estado_ejecucion in ["ACEPTADA", "RECHAZADA"]:
            self.motor = None
            self._limpiar_historial()
            self._cambiar_estado_lbl("CARGADO" if self.resultado_parser else "NO INICIADA", "blue")
            self._actualizar_botones()

        cadena = self.var_cadena.get().strip()
        cinta_sim = {i: c for i, c in enumerate(cadena)}
        simbolo = cadena[0] if cadena else "B"

        cfg_temp = Configuracion(
            paso=0,
            estado="q0",
            memoria=MEMORIA_VACIA,
            posicion_cabezal=0,
            cinta=cinta_sim,
            simbolo_leido=simbolo,
            transicion_aplicada=None,
            transicion_pendiente=None,
            motivo_detencion=None,
        )
        self._dibujar_cinta_visual(cfg_temp)
        self._actualizar_botones()

    def _cargar_archivo(self) -> None:
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de transiciones con memoria",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return

        try:
            self.resultado_parser = parsear_archivo(ruta)
            self.nombre_archivo_actual = os.path.basename(ruta)
            self.lbl_archivo.config(text=self.nombre_archivo_actual, foreground="black")
            self._limpiar_historial()
            self._actualizar_tabla()
            self._actualizar_diagrama()
            self._actualizar_botones()
            self._cambiar_estado_lbl("CARGADO", "blue")
            self._actualizar_cinta_previa()

        except ErrorArchivo as e:
            messagebox.showerror("Error de Archivo", str(e))
        except ErrorParser as e:
            messagebox.showerror("Error en Archivo de Reglas", f"{e}")
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))

    def _actualizar_tabla(self) -> None:
        self.canvas_tabla.delete("all")
        if not self.resultado_parser:
            return

        gen = GeneradorTablaMemoria(self.resultado_parser)
        columnas = gen.obtener_columnas()
        filas = gen.obtener_filas()

        ancho_estado = 110
        ancho_celda = 145
        alto_celda = 30
        margen = 10
        anchos = [ancho_estado] + [ancho_celda] * (len(columnas) - 1)

        # Encabezados
        x = margen
        for i, col in enumerate(columnas):
            w = anchos[i]
            self.canvas_tabla.create_rectangle(
                x, margen, x + w, margen + alto_celda,
                fill="#DCE6F1", outline="#667085", width=1,
            )
            self.canvas_tabla.create_text(
                x + w / 2, margen + alto_celda / 2,
                text=col, font=("Consolas", 10, "bold"), fill="#1F2937",
            )
            x += w

        # Filas
        for r_idx, fila in enumerate(filas):
            x = margen
            y = margen + (r_idx + 1) * alto_celda
            fondo = "#F0F8FF" if r_idx % 2 == 0 else "#FFFFFF"

            for c_idx, val in enumerate(fila):
                w = anchos[c_idx]
                self.canvas_tabla.create_rectangle(
                    x, y, x + w, y + alto_celda,
                    fill=fondo, outline="#98A2B3", width=1,
                )
                self.canvas_tabla.create_text(
                    x + w / 2, y + alto_celda / 2,
                    text=val, font=("Consolas", 10), fill="#1F2937",
                )
                x += w

        ancho_tot = margen * 2 + sum(anchos)
        alto_tot = margen * 2 + (len(filas) + 1) * alto_celda
        self.canvas_tabla.configure(scrollregion=(0, 0, ancho_tot, alto_tot))

    def _actualizar_diagrama(self) -> None:
        if not self.resultado_parser:
            return

        self.canvas_diagrama.delete("all")
        gen = GeneradorDiagramaMemoria(self.resultado_parser)
        dot = gen.construir_grafo()

        if dot is None:
            self.lbl_diagrama_fallback.config(
                text="Libreria Graphviz no instalada.\nDiagrama deshabilitado."
            )
            self.lbl_diagrama_fallback.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            return

        try:
            ruta_temp = os.path.join(tempfile.gettempdir(), ".mt_memoria_diagrama")
            ruta_img = dot.render(filename=ruta_temp, format="png", cleanup=True)
            self._img_diagrama = tk.PhotoImage(file=ruta_img)
            self.lbl_diagrama_fallback.place_forget()
            self.canvas_diagrama.create_image(0, 0, anchor=tk.NW, image=self._img_diagrama)
            self.canvas_diagrama.config(scrollregion=self.canvas_diagrama.bbox(tk.ALL))
        except ExecutableNotFound:
            self.lbl_diagrama_fallback.config(
                text="Herramienta 'dot' de Graphviz no encontrada en el sistema."
            )
            self.lbl_diagrama_fallback.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _preparar_motor(self) -> bool:
        if not self.resultado_parser:
            return False

        cadena = self.var_cadena.get().strip()
        if not cadena:
            messagebox.showwarning("Cadena vacia", "Por favor introduzca una cadena de entrada.")
            return False

        self.motor = MaquinaTuringMemoria(self.resultado_parser.transiciones)
        self.motor.iniciar(cadena)
        self._limpiar_historial()
        return True

    def _iniciar_maquina(self) -> None:
        if self._preparar_motor():
            if self.motor.estado_ejecucion != "EN_CURSO":
                self._refrescar_ui_desde_motor()
                self._actualizar_botones()
            else:
                self._ejecutar_todo()

    def _paso_a_paso(self) -> None:
        if not self.motor or self.motor.estado_ejecucion not in ["EN_CURSO", "DETENIDA"]:
            if not self._preparar_motor():
                return
            if self.motor.estado_ejecucion != "EN_CURSO":
                self._refrescar_ui_desde_motor()
                self._actualizar_botones()
                return

        if self.motor.estado_ejecucion == "EN_CURSO":
            self.motor.paso()
            self._refrescar_ui_desde_motor()
            self._actualizar_botones()

    def _ejecutar_todo(self) -> None:
        if not self.motor or self.motor.estado_ejecucion != "EN_CURSO":
            return

        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_paso.config(state=tk.DISABLED)
        self.entry_cadena.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

        while not self.cola_actualizaciones.empty():
            self.cola_actualizaciones.get()
        self.evento_detener.clear()

        self.hilo_ejecucion = threading.Thread(target=self._bucle_hilo, daemon=True)
        self.hilo_ejecucion.start()
        self._procesar_cola()

    def _bucle_hilo(self) -> None:
        velocidades = {"Lenta": 1.0, "Media": 0.5, "Rapida": 0.1, "Inmediata": 0.0}
        delay = velocidades.get(self.var_velocidad.get(), 0.5)

        while not self.evento_detener.is_set():
            continuar = self.motor.paso()
            self.cola_actualizaciones.put("PASO")
            if not continuar:
                break
            if delay > 0:
                time.sleep(delay)

        if self.evento_detener.is_set():
            self.motor.detener()
            self.cola_actualizaciones.put("PASO")

        self.cola_actualizaciones.put("FIN")

    def _procesar_cola(self) -> None:
        try:
            while True:
                msg = self.cola_actualizaciones.get_nowait()
                if msg == "PASO":
                    self._refrescar_ui_desde_motor()
                elif msg == "FIN":
                    self._actualizar_botones()
                    return
        except queue.Empty:
            pass
        self.root.after(40, self._procesar_cola)

    def _detener(self) -> None:
        if self.hilo_ejecucion and self.hilo_ejecucion.is_alive():
            self.evento_detener.set()

    def _refrescar_ui_desde_motor(self) -> None:
        if not self.motor or not self.motor.historial:
            return

        cfg_ultima = self.motor.historial[-1]
        self._dibujar_cinta_visual(cfg_ultima)

        for i in range(self.ultimo_paso_mostrado + 1, len(self.motor.historial)):
            cfg = self.motor.historial[i]
            cinta_dest = cfg.representacion_cinta_destacada()
            accion = (
                cfg.transicion_aplicada.formato_accion()
                if cfg.transicion_aplicada
                else (cfg.transicion_pendiente.formato_accion() if cfg.transicion_pendiente else "-")
            )
            tag = "fila_par" if cfg.paso % 2 == 0 else "fila_impar"

            item = self.tree_historial.insert(
                "",
                tk.END,
                values=(
                    cfg.paso,
                    cfg.estado,
                    cfg.memoria,
                    cinta_dest,
                    accion,
                ),
                tags=(tag,),
            )
            self.tree_historial.see(item)

            if i == len(self.motor.historial) - 1:
                if self.motor.estado_ejecucion == "ACEPTADA":
                    self.lbl_solucion.config(
                        text=f"✓ CADENA ACEPTADA (Estado: {cfg.estado}, Memoria: {cfg.memoria})",
                        foreground="green",
                    )
                elif self.motor.estado_ejecucion == "RECHAZADA":
                    self.lbl_solucion.config(
                        text=f"✗ CADENA RECHAZADA (En paso {cfg.paso})",
                        foreground="red",
                    )
                elif self.motor.estado_ejecucion == "DETENIDA":
                    self.lbl_solucion.config(
                        text="DETENIDA POR EL USUARIO",
                        foreground="purple",
                    )

        self.ultimo_paso_mostrado = len(self.motor.historial) - 1

        est = self.motor.estado_ejecucion
        color = {
            "EN_CURSO": "orange",
            "ACEPTADA": "green",
            "RECHAZADA": "red",
            "DETENIDA": "purple",
        }.get(est, "black")
        self._cambiar_estado_lbl(est, color)

    def _dibujar_cinta_visual(self, cfg: Configuracion) -> None:
        self.canvas_cinta.delete("all")
        indices = list(cfg.cinta.keys()) if cfg.cinta else [0]

        min_idx = min(indices + [cfg.posicion_cabezal])
        max_idx = max(indices + [cfg.posicion_cabezal])
        start = min_idx - 2
        end = max_idx + 2

        celda_w = 52
        celda_h = 50
        pad_x = 25
        pad_y = 55

        # Indicador de estado y memoria en el cabezal superior
        info_cabezal = f"Estado: {cfg.estado}  |  Memoria m: {cfg.memoria}"
        self.canvas_cinta.create_text(
            pad_x + 10,
            20,
            text=info_cabezal,
            font=("Consolas", 12, "bold"),
            anchor=tk.W,
            fill="#1E3A8A",
        )

        x = pad_x
        for i in range(start, end + 1):
            simbolo = cfg.cinta.get(i, "B")
            es_cabezal = (i == cfg.posicion_cabezal)

            color_fondo = "#E0F2FE" if es_cabezal else "#FFFFFF"
            color_borde = "#DC2626" if es_cabezal else "#334155"
            grosor = 2 if es_cabezal else 1

            self.canvas_cinta.create_rectangle(
                x, pad_y, x + celda_w, pad_y + celda_h,
                fill=color_fondo, outline=color_borde, width=grosor,
            )
            self.canvas_cinta.create_text(
                x + celda_w / 2, pad_y + celda_h / 2,
                text=simbolo, font=("Consolas", 15, "bold"),
            )

            # Flecha indicadora del cabezal y tarjeta de memoria
            if es_cabezal:
                self.canvas_cinta.create_text(
                    x + celda_w / 2, pad_y + celda_h + 12,
                    text="▲", font=("Consolas", 15, "bold"), fill="#DC2626",
                )
                self.canvas_cinta.create_text(
                    x + celda_w / 2, pad_y + celda_h + 30,
                    text=f"q: {cfg.estado}", font=("Consolas", 11, "bold"), fill="#DC2626",
                )
                self.canvas_cinta.create_text(
                    x + celda_w / 2, pad_y + celda_h + 46,
                    text=f"m: {cfg.memoria}", font=("Consolas", 10, "bold"), fill="#2563EB",
                )

            x += celda_w

        self.canvas_cinta.config(scrollregion=self.canvas_cinta.bbox(tk.ALL))
        self.canvas_cinta.update_idletasks()
        bbox = self.canvas_cinta.bbox(tk.ALL)
        w_visible = self.canvas_cinta.winfo_width()

        if bbox and w_visible > 1:
            total_w = bbox[2]
            if total_w > w_visible:
                idx_relativo = cfg.posicion_cabezal - start
                pos_x_cabezal = pad_x + (idx_relativo * celda_w) + (celda_w / 2)
                fraccion = max(0.0, min(1.0, (pos_x_cabezal - (w_visible / 2)) / total_w))
                self.canvas_cinta.xview_moveto(fraccion)

    def _limpiar_historial(self) -> None:
        self.ultimo_paso_mostrado = -1
        self.lbl_solucion.config(text="")
        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)

    def _actualizar_botones(self) -> None:
        cadena_valida = bool(self.var_cadena.get().strip())
        archivo_cargado = bool(self.resultado_parser)

        if not self.motor or self.motor.estado_ejecucion in ["NO_INICIADA", "DETENIDA", "ACEPTADA", "RECHAZADA"]:
            estado_btn = tk.NORMAL if (cadena_valida and archivo_cargado) else tk.DISABLED
            self.btn_iniciar.config(state=estado_btn)
            self.btn_paso.config(state=estado_btn)
            self.btn_stop.config(state=tk.DISABLED)
            self.entry_cadena.config(state=tk.NORMAL)

            if self.motor and self.motor.estado_ejecucion in ["ACEPTADA", "RECHAZADA", "DETENIDA"]:
                self.btn_exportar.config(state=tk.NORMAL)
            else:
                self.btn_exportar.config(state=tk.DISABLED)
        elif self.hilo_ejecucion and self.hilo_ejecucion.is_alive():
            self.btn_iniciar.config(state=tk.DISABLED)
            self.btn_paso.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.entry_cadena.config(state=tk.DISABLED)
            self.btn_exportar.config(state=tk.DISABLED)
        else:
            self.btn_iniciar.config(state=tk.DISABLED)
            self.btn_paso.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.entry_cadena.config(state=tk.NORMAL)
            self.btn_exportar.config(state=tk.DISABLED)

    def _cambiar_estado_lbl(self, texto: str, color: str) -> None:
        self.lbl_estado.config(text=texto, foreground=color)

    def _exportar_historial(self) -> None:
        if not self.motor or not self.motor.historial:
            messagebox.showwarning("Historial Vacio", "No hay descripciones para exportar.")
            return

        cadena = self.var_cadena.get().strip()
        nombre_base = self.nombre_archivo_actual.replace(".txt", "") if self.nombre_archivo_actual else "mt_memoria"
        nombre_sugerido = f"resultado_{nombre_base}_{cadena}.txt"

        ruta = filedialog.asksaveasfilename(
            initialfile=nombre_sugerido,
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")],
            title="Guardar Historial de Ejecucion",
        )
        if not ruta:
            return

        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("SIMULADOR DE MAQUINA DE TURING CON MEMORIA INTERNA FINITA\n")
                f.write("========================================================================================\n")
                f.write(f"Archivo de Reglas: {self.nombre_archivo_actual}\n")
                f.write(f"Cadena Evaluada: {cadena}\n")
                f.write(f"Resultado Final: {self.motor.estado_ejecucion}\n")
                f.write("========================================================================================\n\n")
                f.write(f"{'Paso':<6}{'Estado':<8}{'Memoria':<10}{'Cinta':<18}{'Pos':<6}{'Accion'}\n")
                f.write("-" * 75 + "\n")

                for cfg in self.motor.historial:
                    cinta_dest = cfg.representacion_cinta_destacada()
                    accion = (
                        cfg.transicion_aplicada.formato_accion()
                        if cfg.transicion_aplicada
                        else (cfg.transicion_pendiente.formato_accion() if cfg.transicion_pendiente else "-")
                    )
                    f.write(
                        f"{cfg.paso:<6}{cfg.estado:<8}{cfg.memoria:<10}{cinta_dest:<18}{cfg.posicion_cabezal:<6}{accion}\n"
                    )

                f.write("-" * 75 + "\n")
                f.write(f"ESTADO FINAL: {self.motor.estado_ejecucion} en {len(self.motor.historial) - 1} pasos.\n")

            messagebox.showinfo("Exportacion Exitosa", f"Historial guardado exitosamente en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al Exportar", str(e))


def run_app() -> None:
    root = tk.Tk()
    app = SimuladorMemoriaApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
