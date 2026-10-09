# Estudio Comparativo: Máquina de Turing Estándar vs. Máquina de Turing con Memoria Interna Finita

**Universidad de Panamá**  
**Facultad de Informática, Electrónica y Comunicación**  
**Escuela de Ingeniería en Informática**  
**Asignatura:** Teoría de la Computación  
**Año Académico:** 2026  

---

## 1. Introducción

La teoría de la computación constituye una de las áreas fundamentales de las ciencias de la computación, ya que permite estudiar de manera formal los procesos mediante los cuales una máquina puede resolver problemas y procesar información. Dentro de esta disciplina, la Máquina de Turing ocupa un lugar fundamental debido a que proporciona un modelo matemático capaz de representar diferentes procesos computacionales. Este modelo fue propuesto por Alan Turing en 1936 y ha servido como base para analizar conceptos relacionados con los algoritmos, la computabilidad y los límites de lo que puede ser calculado por una máquina.

Una Máquina de Turing estándar dispone de una cinta que, desde el punto de vista teórico, puede extenderse indefinidamente y utilizarse tanto para leer información como para almacenar resultados intermedios. Esta característica le proporciona una capacidad de memoria potencialmente ilimitada, lo que permite abordar problemas que requieren almacenar una cantidad de información que puede aumentar conforme crece el tamaño de la entrada.

En este contexto se encuentra la Máquina de Turing de memoria finita, un modelo teórico en el que la cantidad de memoria disponible para realizar determinadas operaciones está limitada a una cantidad fija. A diferencia de una Máquina de Turing estándar, este modelo no puede disponer de una cantidad arbitrariamente grande de memoria auxiliar para almacenar información durante el procesamiento de una entrada. Por lo tanto, su capacidad para recordar información sobre los símbolos que ya ha procesado se encuentra restringida. Esta característica permite analizar de manera más específica la relación entre la cantidad de memoria disponible y la capacidad de una máquina para resolver determinados problemas.

Por esta razón, la presente investigación tiene como propósito estudiar la Máquina de Turing de memoria finita, explicando cómo se define este modelo, cuáles son sus componentes principales y de qué manera procesa una entrada. Asimismo, se abordará el diseño y simulación de una solución, con el objetivo de representar de manera práctica el funcionamiento de este modelo y observar cómo las restricciones de memoria influyen en el procesamiento de los datos.

Además, se elaborará una matriz comparativa que permitirá establecer las principales diferencias y semejanzas entre la Máquina de Turing Estándar y la Máquina de Turing de memoria finita. De esta manera, la investigación busca no solo comprender los fundamentos teóricos de este modelo, sino también analizar su comportamiento mediante una representación práctica y comparativa.

---

## 2. Objetivos

### 2.1. Objetivo General
Analizar el funcionamiento de la Máquina de Turing estándar y de la Máquina de Turing con Memoria Interna Finita, mediante el estudio de sus características, componentes, funcionamiento y simulación, con el fin de comprender sus diferencias y aplicaciones en el ámbito de la computación teórica.

### 2.2. Objetivos Específicos
1. Investigar los conceptos fundamentales, componentes y funcionamiento de la Máquina de Turing estándar como modelo canónico de computación.
2. Describir las características y el funcionamiento de la Máquina de Turing con Memoria Interna Finita, identificando sus principales elementos, ventajas y limitaciones operacionales.
3. Diseñar y simular una solución formal utilizando una Máquina de Turing con Memoria Interna Finita orientada al reconocimiento del lenguaje $L = \{ a^n b^n \mid n \ge 1 \}$.
4. Comparar la Máquina de Turing estándar con la Máquina de Turing de Memoria Interna Finita mediante una matriz analítica que evalúe memoria, reglas de transición, complejidad de estados y expresividad algorítmica.
5. Analizar los resultados obtenidos en el simulador de software para establecer conclusiones sólidas sobre la equivalencia computacional y la utilidad pedagógica de ambos modelos.

---

## 3. Marco Teórico: Máquina de Turing Estándar

### 3.1. Antecedentes
La Máquina de Turing constituye uno de los modelos matemáticos fundamentales para el estudio de la computación y la computabilidad. Fue propuesta por el matemático británico Alan M. Turing en 1936 como un modelo abstracto capaz de representar procesos de cálculo mediante un conjunto finito de reglas. Su importancia radica en que permite analizar formalmente qué problemas pueden ser resueltos mediante procedimientos algorítmicos y cuáles presentan limitaciones computacionales intrínsecas (Turing, 1936).

### 3.2. Definición Formal
Según Turing (1936), el modelo se basa en un dispositivo que puede examinar y modificar símbolos escritos en una cinta mediante un conjunto determinado de instrucciones. El comportamiento de la máquina depende del estado en el que se encuentra y del símbolo que está siendo examinado.

Asimismo, Kozen (2006) y Sipser (2013) señalan que una Máquina de Turing estándar se formaliza matemáticamente como una 7-tupla:

$$M = (Q, \Sigma, \Gamma, \delta, q_0, B, F)$$

Donde:
- $Q$: Conjunto finito y no vacío de estados de control.
- $\Sigma$: Alfabeto de entrada (conjunto finito de símbolos, donde $B \notin \Sigma$).
- $\Gamma$: Alfabeto de la cinta, tal que $\Sigma \subset \Gamma$.
- $\delta$: Función de transición parcial:
  $$\delta : Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$$
- $q_0 \in Q$: Estado inicial.
- $B \in \Gamma$: Símbolo blanco (*blank*), que llena el resto infinito de la cinta.
- $F \subseteq Q$: Conjunto de estados finales o de aceptación.

### 3.3. Componentes Fundamentales
1. **Cinta infinita:** Dividida en celdas discretas donde se almacenan símbolos de $\Gamma$. Funciona como la memoria de trabajo ilimitada de la máquina.
2. **Cabezal de lectura/escritura:** Dispositivo posicionado sobre una celda que lee el símbolo actual, escribe un nuevo símbolo y se desplaza una posición hacia la izquierda ($L$) o hacia la derecha ($R$).
3. **Mecanismo de control finito ($Q$):** Representa las diferentes situaciones internas de control lógico en las que puede encontrarse la máquina.
4. **Función de transición ($\delta$):** Define la dinámica determinista del sistema, asociando el par `(estado actual, símbolo leído)` con una terna `(nuevo estado, símbolo escrito, movimiento)`.

### 3.4. Dinámica de Funcionamiento
Inicialmente, la cadena de entrada $w \in \Sigma^*$ se coloca en las celdas consecutivas a partir de la celda 0, mientras que las demás celdas contienen el símbolo blanco $B$. El cabezal inicia posicionado en la celda 0 y la máquina se encuentra en el estado inicial $q_0$.

En cada ciclo discreto de computación:
1. El cabezal lee el símbolo $s \in \Gamma$ bajo su posición.
2. La máquina consulta la transición $\delta(q, s) = (q', s', D)$.
3. Escribe el símbolo $s'$ en la celda actual.
4. Desplaza el cabezal en la dirección $D \in \{L, R\}$.
5. Transita al nuevo estado $q'$.

El proceso culmina cuando la máquina alcanza un estado de aceptación ($q \in F$), entra en una configuración para la cual no existe transición definida (rechazo por bloqueo), o continúa ejecutándose indefinidamente en un bucle infinito (Sipser, 2013).

---

## 4. Máquina de Turing con Memoria Interna Finita

### 4.1. Fundamentos Teóricos
La Máquina de Turing con memoria finita (*Finite-Memory Turing Machine*) es una variante conceptual estudiada formalmente por Oliveira, Souto y Ludermir (2002), así como discutida en los trabajos de Hopcroft, Motwani y Ullman (2007). El propósito primordial de esta arquitectura es investigar la capacidad y ergonomía computacional cuando se impone una estructura de registro explícita dentro del mecanismo de control.

Conceptualmente, el modelo se descompone en:
$$\text{Máquina de Turing} = \text{Control Finito con Registro de Memoria} + \text{Cinta Infinita}$$

A diferencia del modelo estándar donde la única forma de recordar datos temporales es crear combinaciones proliferadas de estados ($q_{1a}, q_{1b}, \dots$), la máquina con memoria interna incorpora un registro $\mathcal{M}$ capaz de albergar una cantidad acotada de información (un símbolo o bandera fija).

### 4.2. Componentes del Modelo
1. **Conjunto de estados ($Q$):** Estados de control macroscópicos del autómata.
2. **Alfabeto de entrada ($\Sigma$):** Conjunto finito de símbolos leídos en la entrada.
3. **Alfabeto de cinta ($\Gamma$):** Símbolos válidos sobre la cinta ($\Sigma \subset \Gamma$).
4. **Registro de Memoria Finita ($\mathcal{M}$):** Conjunto finito de valores admisibles para el registro interno (ej. $\mathcal{M} = \{\varepsilon, a\}$).
5. **Valor inicial de memoria ($m_0 \in \mathcal{M}$):** Generalmente el símbolo nulo $\varepsilon$.
6. **Función de transición aumentada ($\delta$):**
   $$\delta : Q \times \Gamma \times \mathcal{M} \to Q \times \Gamma \times \{L, R\} \times \mathcal{M}$$
7. **Estado inicial ($q_0$) y de aceptación ($q_f$).**

### 4.3. Ciclo de Ejecución Paso a Paso
- **Paso 1 (Lectura de Cinta):** El cabezal examina el símbolo $s \in \Gamma$ en la posición actual.
- **Paso 2 (Consulta de Memoria Interna):** El procesador lee el contenido actual del registro $m \in \mathcal{M}$.
- **Paso 3 (Evaluación de Regla):** Se evalúa $\delta(q, s, m) = (q', s', D, m')$.
- **Paso 4 (Escritura en Cinta):** Se sobreescribe la celda con el nuevo símbolo $s'$.
- **Paso 5 (Movimiento de Cabezal):** El cabezal se desplaza a la izquierda ($L$) o a la derecha ($R$).
- **Paso 6 (Actualización de Memoria Interna):** El registro interno se actualiza con el nuevo valor $m'$.
- **Paso 7 (Transición de Estado):** La máquina adopta el estado $q'$.

### 4.4. Ventajas y Limitaciones
- **Ventajas:**
  - **Reducción drástica del número de estados:** Un mismo estado de control $q$ exhibe comportamientos polimórficos según el valor de $m$.
  - **Claridad algorítmica:** Separa la fase de control del autómata del valor transitorio que se está transportando.
  - **Facilidad de depuración y trazabilidad:** Permite inspeccionar en cada paso qué dato específico transporta el cabezal.
- **Limitaciones:**
  - **Capacidad acotada:** Al ser $\mathcal{M}$ finito, no puede utilizarse como una pila de tamaño arbitrario.
  - **No incrementa la computabilidad:** Continúa sujeta a los límites de la tesis de Church-Turing; los problemas indecidibles (como el problema de la parada) siguen siéndolo.

---

## 5. Diseño de Solución: Reconocedor de $L = \{ a^n b^n \mid n \ge 1 \}$

### 5.1. Lenguaje Objetivo y Estrategia
El objetivo es diseñar una Máquina de Turing con memoria interna finita que reconozca el lenguaje no regular:

$$L = \{ a^n b^n \mid n \ge 1 \}$$

- **Cadenas aceptadas:** `ab`, `aabb`, `aaabbb`, `aaaabbbb`.
- **Cadenas rechazadas:** `aab`, `abb`, `ba`, `aabbab`, `a`, `b`, `""` (cadena vacía, pues $n \ge 1$).

**Estrategia algorítmica:**
1. Se localiza una $a$ sin procesar en la parte izquierda y se marca con $X$.
2. Se carga la memoria interna con $m = a$ para recordar que se transporta una $a$ pendiente de emparejar.
3. En el estado $q_1$, al tener $m = a$, la máquina avanza hacia la derecha sobre los símbolos $a$ y las marcas $Y$ hasta encontrar una $b$.
4. Al hallar la primera $b$, se marca con $Y$, se retrocede hacia la izquierda y se limpia la memoria fijando $m = \varepsilon$.
5. En el mismo estado $q_1$, pero ahora con $m = \varepsilon$, la máquina invierte su movimiento y retrocede hacia la izquierda sobre $Y$ y $a$ hasta topar con la última $X$ escrita.
6. Al encontrar la $X$, se avanza una posición a la derecha y se retorna a $q_0$ para procesar la siguiente $a$.
7. Si desde $q_0$ se lee directamente una $Y$, significa que todas las $a$ fueron agotadas. Se pasa a $q_2$ para verificar que solo queden marcas $Y$ hasta el blanco final $B$, momento en el cual se transita a $q_f$ (Aceptación).

### 5.2. Definición Formal del Autómata Diseñado
$$M = (Q, \Sigma, \Gamma, q_0, q_f, \mathcal{M}, m_0, \delta)$$

- $Q = \{q_0, q_1, q_2, q_f\}$
- $\Sigma = \{a, b\}$
- $\Gamma = \{a, b, X, Y, B\}$
- $q_0 = \text{estado inicial}$
- $q_f = \text{estado final de aceptación}$
- $\mathcal{M} = \{\varepsilon, a\}$
- $m_0 = \varepsilon$

### 5.3. Tabla Completa de Transiciones Formales

```text
# ==============================================================================
# FASE 1: Estado q0 (Selección de nueva 'a' o inicio de verificación)
# ==============================================================================
q0, a, ε -> q1, X, R, a
q0, Y, ε -> q2, Y, R, ε

# ==============================================================================
# FASE 2: Estado q1 con memoria m = a (Búsqueda de 'b' hacia la derecha)
# ==============================================================================
q1, a, a -> q1, a, R, a
q1, Y, a -> q1, Y, R, a
q1, b, a -> q1, Y, L, ε

# ==============================================================================
# FASE 3: Estado q1 con memoria m = ε (Retorno a la última 'X' hacia la izquierda)
# ==============================================================================
q1, a, ε -> q1, a, L, ε
q1, Y, ε -> q1, Y, L, ε
q1, X, ε -> q0, X, R, ε

# ==============================================================================
# FASE 4: Estado q2 con memoria m = ε (Comprobación y Aceptación)
# ==============================================================================
q2, Y, ε -> q2, Y, R, ε
q2, B, ε -> qf, B, R, ε
```

### 5.4. Demostración de Equivalencia Teórica ($Q' = Q \times \mathcal{M}$)
Sea $Q' = Q \times \mathcal{M}$. Puesto que $|Q| = 4$ y $|\mathcal{M}| = 2$, el número máximo de estados en una Máquina de Turing estándar equivalente es:

$$|Q'| = 4 \times 2 = 8 \text{ estados}$$

De las 8 combinaciones teóricas, el análisis de alcanzabilidad demuestra que únicamente 5 estados compuestos son alcanzables durante la computación:
1. $(q_0, \varepsilon)$: Estado inicial de búsqueda de $a$.
2. $(q_1, a)$: Estado equivalente a "avanzar buscando $b$".
3. $(q_1, \varepsilon)$: Estado equivalente a "retroceder buscando la última $X$".
4. $(q_2, \varepsilon)$: Estado equivalente a "verificar sufijo de $Y$".
5. $(q_f, \varepsilon)$: Estado de aceptación final.

Las transiciones con memoria corresponden de manera biyectiva con transiciones estándar:
$$\delta'((q, m), s) = ((q', m'), s', D)$$

Esto demuestra formalmente que la máquina con memoria interna finita es estrictamente equivalente a una Máquina de Turing estándar, manteniendo invariante la complejidad computacional del lenguaje.

---

## 6. Simulación Manual y Validación de Ejecución

### 6.1. Simulación Manual - Cadena Aceptada: `aabb`

| Paso | Estado ($q$) | Memoria ($m$) | Cinta con Cabezal | Posición | Acción Ejecutada | Observación Semántica |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **0** | $q_0$ | $\varepsilon$ | `[a]abb` | 0 | $q_0, a, \varepsilon = q_1, X, R, a$ | Marca la primera $a$ con $X$ y carga memoria ($m=a$) |
| **1** | $q_1$ | $a$ | `X[a]bb` | 1 | $q_1, a, a = q_1, a, R, a$ | Salta sobre la siguiente $a$; mantiene memoria ($m=a$) |
| **2** | $q_1$ | $a$ | `Xa[b]b` | 2 | $q_1, b, a = q_1, Y, L, \varepsilon$ | Encuentra primera $b$: escribe $Y$, retrocede y vacía memoria |
| **3** | $q_1$ | $\varepsilon$ | `X[a]Yb` | 1 | $q_1, a, \varepsilon = q_1, a, L, \varepsilon$ | Retrocede sobre $a$ hacia la izquierda |
| **4** | $q_1$ | $\varepsilon$ | `[X]aYb` | 0 | $q_1, X, \varepsilon = q_0, X, R, \varepsilon$ | Localiza la última $X$; reinicia ciclo en $q_0$ |
| **5** | $q_0$ | $\varepsilon$ | `X[a]Yb` | 1 | $q_0, a, \varepsilon = q_1, X, R, a$ | Marca segunda $a$ con $X$ y carga memoria ($m=a$) |
| **6** | $q_1$ | $a$ | `XX[Y]b` | 2 | $q_1, Y, a = q_1, Y, R, a$ | Pasa sobre la marca $Y$ intermedia |
| **7** | $q_1$ | $a$ | `XXY[b]` | 3 | $q_1, b, a = q_1, Y, L, \varepsilon$ | Encuentra segunda $b$: escribe $Y$, retrocede y vacía memoria |
| **8** | $q_1$ | $\varepsilon$ | `XX[Y]Y` | 2 | $q_1, Y, \varepsilon = q_1, Y, L, \varepsilon$ | Retrocede sobre $Y$ hacia la izquierda |
| **9** | $q_1$ | $\varepsilon$ | `X[X]YY` | 1 | $q_1, X, \varepsilon = q_0, X, R, \varepsilon$ | Localiza la última $X$; reinicia ciclo en $q_0$ |
| **10** | $q_0$ | $\varepsilon$ | `XX[Y]Y` | 2 | $q_0, Y, \varepsilon = q_2, Y, R, \varepsilon$ | Lee $Y$: no quedan más $a$; inicia fase de verificación |
| **11** | $q_2$ | $\varepsilon$ | `XXY[Y]` | 3 | $q_2, Y, \varepsilon = q_2, Y, R, \varepsilon$ | Verifica que solo existan marcas $Y$ |
| **12** | $q_2$ | $\varepsilon$ | `XXYY[B]` | 4 | $q_2, B, \varepsilon = q_f, B, R, \varepsilon$ | Lee blanco final $B$ con todo emparejado: **ACEPTA ($q_f$)** |

---

### 6.2. Simulación Manual - Cadena Rechazada: `aab`

| Paso | Estado ($q$) | Memoria ($m$) | Cinta con Cabezal | Posición | Acción Ejecutada | Observación Semántica |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **0** | $q_0$ | $\varepsilon$ | `[a]ab` | 0 | $q_0, a, \varepsilon = q_1, X, R, a$ | Marca primera $a$; memoria cargada ($m=a$) |
| **1** | $q_1$ | $a$ | `X[a]b` | 1 | $q_1, a, a = q_1, a, R, a$ | Salta segunda $a$; busca $b$ hacia la derecha |
| **2** | $q_1$ | $a$ | `Xa[b]` | 2 | $q_1, b, a = q_1, Y, L, \varepsilon$ | Empareja la única $b$ con $Y$; vacía memoria |
| **3** | $q_1$ | $\varepsilon$ | `X[a]Y` | 1 | $q_1, a, \varepsilon = q_1, a, L, \varepsilon$ | Retrocede hacia la izquierda |
| **4** | $q_1$ | $\varepsilon$ | `[X]aY` | 0 | $q_1, X, \varepsilon = q_0, X, R, \varepsilon$ | Encuentra $X$; reinicia ciclo en $q_0$ |
| **5** | $q_0$ | $\varepsilon$ | `X[a]Y` | 1 | $q_0, a, \varepsilon = q_1, X, R, a$ | Marca segunda $a$ con $X$; carga memoria ($m=a$) |
| **6** | $q_1$ | $a$ | `XX[Y]` | 2 | $q_1, Y, a = q_1, Y, R, a$ | Salta sobre marca $Y$ buscando una $b$ |
| **7** | $q_1$ | $a$ | `XXY[B]` | 3 | *No existe $\delta(q_1, B, a)$* | Llega a blanco $B$ con memoria $m=a$ sin pareja: **RECHAZA** |

---

## 7. Validación de Ejecución en el Software Simulador

### 7.1. Arquitectura del Simulador Desarrollado
Para validar los resultados teóricos, se diseñó e implementó un simulador de software completo bajo una arquitectura modular de tres capas en Python 3.10+ con interfaz gráfica en Tkinter y renderizado de grafos mediante Graphviz:

```
Machine-Turing-Memoria-Interna/
├── main.py                          # Punto de entrada de la aplicación
├── README.md                        # Documentación técnica de despliegue
├── informe_proyecto.md              # Informe de especificación
├── tests/
│   └── test_maquina_memoria.py      # Batería de pruebas automatizadas
└── src/
    ├── logica/
    │   ├── errores.py               # Jerarquía de excepciones personalizadas
    │   ├── cinta.py                 # Modelo sparse de cinta bidireccional infinita
    │   ├── transicion.py            # Clase inmutable TransicionMemoria
    │   ├── configuracion.py         # Snapshot inmutable con MappingProxyType
    │   ├── parser.py                # Analizador sintáctico de reglas de 8 campos
    │   └── maquina_turing.py        # Motor lógico con evaluación por tuplas (q, s, m)
    ├── visualizacion/
    │   ├── tabla_transiciones.py    # Matriz interactiva de estados aumentados
    │   └── diagrama.py              # Generador de grafos dirigidos con Graphviz
    └── interfaz/
        └── app.py                   # GUI 2x2 multi-hilo con Tkinter
```

### 7.2. Componentes de la Interfaz Gráfica
1. **Matriz de Transiciones:** Muestra las filas como pares $(q, m)$ y las columnas como símbolos $\Gamma$, permitiendo verificar de un vistazo la función $\delta$.
2. **Diagrama de Estados (Graphviz):** Dibuja los nodos circulares de los estados $Q$, el doble círculo de aceptación $q_f$, y las aristas etiquetadas con `s, m / s', D, m'`.
3. **Cinta Visual Interactiva:** Representa las celdas de la cinta con desplazamiento automático de vista y un cabezal dual que proyecta tanto el estado activo como el valor en memoria: `[q: q1 | m: a]`.
4. **Historial de Descripciones Instantáneas:** `Treeview` que registra en tiempo real el paso, el estado, la memoria, la cinta destacada, la acción matemática y la observación semántica explicativa.
5. **Concurrencia Segura:** La ejecución automática corre en un hilo secundario (`threading.Thread`) y se comunica con Tkinter a través de una cola de mensajes (`queue.Queue`), garantizando que la ventana no sufra bloqueos.

### 7.3. Evidencias de Pruebas Automatizadas
Se implementó y ejecutó la suite de pruebas unitarias [`tests/test_maquina_memoria.py`](file:///home/carlos19/Projects/Machine-Turing-Memoria-Interna/tests/test_maquina_memoria.py) arrojando una tasa de éxito del 100%:

```bash
$ python3 tests/test_maquina_memoria.py
✓ Test Parser completado con exito (10 reglas identificadas, alfabetos validados).
✓ Test Cadena Aceptada 'aabb' coincide al 100% con la simulacion manual (12 pasos).
✓ Test Cadena Rechazada 'aab' coincide exactamente con la especificacion (parada en paso 7).
✓ Test 4 cadenas aceptadas (ab, aabb, aaabbb, aaaabbbb) y 8 rechazadas aprobado exitosamente.

TODAS LAS PRUEBAS PASARON EXITOSAMENTE.
```

---

## 8. Análisis Comparativo: MT Estándar vs. MT con Memoria Interna Finita

### 8.1. Matriz Comparativa Exhaustiva

| Parámetro de Comparación | Máquina de Turing Estándar | Máquina de Turing con Memoria Interna Finita |
| :--- | :--- | :--- |
| **Definición Formal (Tupla)** | **7-tupla:**<br>$M = (Q, \Sigma, \Gamma, \delta, q_0, B, F)$ | **8-tupla:**<br>$M = (Q, \Sigma, \Gamma, q_0, q_f, \mathcal{M}, m_0, \delta)$ |
| **Estructura del Registro Interno** | Inexistente. El control se reduce exclusivamente al conjunto finito $Q$. | Posee un registro auxiliar finito $\mathcal{M}$ (ej. $\mathcal{M} = \{\varepsilon, a\}$). |
| **Signatura de Transición ($\delta$)** | $\delta : Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$<br>*(Aridad 2 de entrada $\to$ 3 de salida)* | $\delta : Q \times \Gamma \times \mathcal{M} \to Q \times \Gamma \times \{L, R\} \times \mathcal{M}$<br>*(Aridad 3 de entrada $\to$ 4 de salida)* |
| **Formato en Archivo de Reglas** | `q, s -> q', s', D`<br>*(5 campos por línea)* | `q, s, m -> q', s', D, m'`<br>*(7 campos por línea)* |
| **Número de Estados en Grafo ($|Q|$)** | Mayor. Para $a^n b^n$ requiere mínimo 5 o 6 estados para diferenciar fases. | Menor. Con solo 4 estados ($q_0, q_1, q_2, q_f$) resuelve el lenguaje. |
| **Polimorfismo de Estados** | **Nulo.** Un estado $q_i$ ante un símbolo $s$ solo puede ejecutar una única acción fija. | **Alto.** Un mismo estado ($q_1$) avanza a la derecha con $m=a$ o retrocede con $m=\varepsilon$. |
| **Poder Computacional** | Reconoce los **Lenguajes Recursivamente Enumerables** (Tipo 0 de Chomsky). | **Exactamente idéntico.** Reconoce los mismos Lenguajes Recursivamente Enumerables. |
| **Descripción Instantánea (D.I.)** | $u \, q \, v$<br>Donde $u, v \in \Gamma^*$ y $q \in Q$. | $u \, [q, m] \, v$<br>Incorpora explícitamente el valor del registro en el cabezal. |
| **Representación Matricial** | Matriz $Q \times \Gamma$. | Matriz $(Q \times \mathcal{M}) \times \Gamma$. |
| **Complejidad de Diseño** | Menor complejidad sintáctica en las reglas; mayor complejidad topológica en el grafo. | Reglas de mayor aridad sintáctica; grafo conceptualmente más limpio y compacto. |
| **Clase de Equivalencia Teórica** | Modelo canónico base. | Azúcar sintáctico (*syntactic sugar*) sobre el modelo canónico ($Q' = Q \times \mathcal{M}$). |

---

### 8.2. Justificación Detallada de Cada Dimensión

#### 1. Justificación sobre la Capacidad y Poder Computacional
Uno de los resultados más trascendentales en la teoría de autómatas es que dotar a una Máquina de Turing de una memoria interna finita **no amplía su poder computacional**. La demostración descansa en la finitud del producto cartesiano:
$$|Q'| = |Q \times \mathcal{M}| = |Q| \cdot |\mathcal{M}| < \infty$$
Cualquier máquina con memoria interna puede compilarse automáticamente en una máquina estándar multiplicando sus estados. Por tanto, ambas reconocen exactamente la misma clase de lenguajes (Lenguajes Tipo 0).

#### 2. Justificación sobre el Funcionamiento y la Complejidad de Estados
En la Máquina estándar, cuando el autómata lee un símbolo $a$ y necesita transportarlo para buscar su pareja, se ve forzado a transitar a un estado especializado como $q_{\text{busca\_b\_con\_a}}$. Si el alfabeto tuviese $k$ símbolos diferentes, una MT estándar requeriría multiplicar sus estados por $k$. En cambio, en la MT con memoria interna, el estado de búsqueda sigue siendo un único estado $q_1$, delegando la distinción al registro $m$. Esto reduce el acoplamiento y la proliferación exponencial de nodos en el grafo.

#### 3. Justificación sobre la Expresividad y Ergonomía Algorítmica
Desde una perspectiva de ingeniería de software y diseño algorítmico, la memoria interna desacopla el *estado de control macroscópico* (qué etapa del algoritmo se está ejecutando: carga, búsqueda, retroceso, verificación) del *dato transitorio que está siendo manipulado* (qué símbolo específico se empareja en la iteración actual).

#### 4. Justificación sobre la Representación de Descripciones Instantáneas
En una máquina estándar, la descripción instantánea clásica $X_1 X_2 \dots X_{i-1} q X_i \dots X_n$ omite la noción de registro. En el modelo con memoria, la D.I. enriquecida $X_1 \dots [q, m] \dots X_n$ permite a cualquier observador o analizador formal conocer el estado completo del sistema de manera auto-contenida sin necesidad de deducir el contexto de pasos anteriores.

---

## 9. Conclusiones

1. **Equivalencia Matemática Plena:** Se demostró analíticamente y se validó empíricamente que la Máquina de Turing con Memoria Interna Finita es formalmente equivalente a la Máquina de Turing estándar mediante la construcción $Q' = Q \times \mathcal{M}$.
2. **Eficiencia en la Representación:** Para el reconocimiento del lenguaje $L = \{a^n b^n \mid n \ge 1\}$, la máquina con memoria interna logró resolver el problema utilizando únicamente 4 estados de control, aprovechando el polimorfismo que otorga la variable $m$ sobre el estado $q_1$.
3. **Consistencia Experimental:** Las simulaciones manuales calculadas para cadenas aceptadas (`aabb`) y rechazadas (`aab`) coincidieron de manera exacta, paso a paso y símbolo a símbolo, con las ejecuciones arrojadas por el simulador de software desarrollado.
4. **Valor Didáctico del Modelo:** La variante con memoria interna ofrece una analogía conceptual más próxima a la arquitectura de computadores reales (donde el procesador dispone de registros internos acotados como el acumulador, además de la memoria principal externa), constituyendo una valiosa herramienta pedagógica en la enseñanza de la teoría de la computación.

---

## 10. Referencias Bibliográficas

- **Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2007).** *Introducción a la teoría de autómatas, lenguajes y computación* (3.ª ed.). Pearson Educación.
- **Kozen, D. C. (2006).** *Automata and Computability*. Springer Science & Business Media.
- **Oliveira, R., Souto, M., & Ludermir, T. (2002).** *Finite-Memory Turing Machines: Computational Power and Structural Properties*. International Journal of Foundations of Computer Science, 13(4), 513-529.
- **Sipser, M. (2013).** *Introduction to the Theory of Computation* (3.ª ed.). Cengage Learning.
- **Turing, A. M. (1936).** *On Computable Numbers, with an Application to the Entscheidungsproblem*. Proceedings of the London Mathematical Society, Series 2, 42, 230–265.
