# Simulador de Máquina de Turing con Memoria Interna Finita

## Descripción del Proyecto
Esta aplicación es una herramienta gráfica e interactiva desarrollada en Python para simular y analizar **Máquinas de Turing con Memoria Interna Finita**, específicamente configurada para reconocer el lenguaje formal:

$$L = \{ a^n b^n \mid n \ge 1 \}$$

La memoria interna finita ($\mathcal{M} = \{\varepsilon, a\}$) permite condicionar las transiciones no solo por el estado de control y el símbolo leído en la cinta, sino también por el valor retenido temporalmente en la memoria, alterando el comportamiento del autómata sin aumentar su clase de poder computacional.

---

## Características Principales
- **Arquitectura Modular de 3 Capas:** Lógica de autómata, visualización de datos e interfaz de usuario completamente desacopladas.
- **Visualización en Cuadrícula 2x2:**
  - **Tabla de Transiciones:** Matriz de estados aumentados $(q, m)$ frente a símbolos de cinta $\Gamma$.
  - **Diagrama de Grafos:** Renderizado automático del autómata con Graphviz.
  - **Cinta Visual Interactiva:** Representación dinámica de la cinta bidireccional con indicador dual del cabezal (`q` y `m`).
  - **Historial Instantáneo:** Tabla detallada que documenta cada paso, estado, memoria, cinta destacada (`Xa[b]b`), acción formal y observación semántica.
- **Ejecución Asíncrona:** Modo paso a paso manual y modo automático multivelocidad ejecutado en hilos secundarios para mantener la fluidez de la interfaz.
- **Exportación de Resultados:** Guardado del historial completo en archivos `.txt`.

---

## Requisitos del Sistema
1. **Python 3.10** o superior.
2. **Tkinter** (incluido por defecto en Python en la mayoría de sistemas operativos).
3. **Graphviz** (opcional pero recomendado para el renderizado del diagrama):
   - En Linux: `sudo apt install graphviz`
   - En Windows: Descargar desde [graphviz.org](https://graphviz.org/) y marcar *"Add Graphviz to system PATH"*.
   - Librería de Python: `pip install graphviz`

---

## Instrucciones de Ejecución

Desde el directorio raíz del proyecto:
```bash
python main.py
```

Para ejecutar las pruebas automatizadas:
```bash
python tests/test_maquina_memoria.py
```

---

## Formato del Archivo de Reglas (`.txt`)
Cada línea de transición sigue la siguiente estructura estricta:
```text
estado_actual, simbolo_leido, memoria_actual -> estado_siguiente, simbolo_escrito, movimiento, memoria_siguiente
```

### Reglas de Diseño:
- **Estado Inicial y Final:** El estado inicial siempre debe ser `q0` (con memoria vacía) y el de parada y aceptación `qf`.
- **Memoria Vacía:** Puede indicarse como `e`, `eps` o el símbolo `ε`.
- **Movimientos:** Solo se permite `R` (Derecha) o `L` (Izquierda).
- **Blanco de Cinta:** Representado por la letra mayúscula `B`.
- **Comentarios:** Líneas comentadas o anotaciones al final de una regla mediante `#`.

### Ejemplo (incluido en `src/ejemplos/an_bn_memoria.txt`):
```text
# Fase 1: Carga en q0
q0, a, e -> q1, X, R, a
q0, Y, e -> q2, Y, R, e

# Fase 2: Busqueda de 'b' con m = a
q1, a, a -> q1, a, R, a
q1, Y, a -> q1, Y, R, a
q1, b, a -> q1, Y, L, e

# Fase 3: Retorno a la ultima 'X' con m = e
q1, a, e -> q1, a, L, e
q1, Y, e -> q1, Y, L, e
q1, X, e -> q0, X, R, e

# Fase 4: Verificacion final
q2, Y, e -> q2, Y, R, e
q2, B, e -> qf, B, R, e
```

---

## Referencia de Desarrollo
**Universidad de Panamá**  
**Facultad de Informática, Electrónica y Comunicación**  
**Ingeniería en Informática**  
**Año:** 2026
