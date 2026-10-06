"""Pruebas automatizadas para el Simulador de Maquina de Turing con Memoria Interna."""

import sys
from pathlib import Path

# Agregar src al path
src_dir = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_dir))

from logica.cinta import Cinta
from logica.parser import parsear_archivo, ResultadoParser
from logica.maquina_turing import MaquinaTuringMemoria
from logica.transicion import MEMORIA_VACIA


def test_parser():
    ruta_reglas = Path(__file__).resolve().parent.parent / "src" / "ejemplos" / "an_bn_memoria.txt"
    resultado = parsear_archivo(ruta_reglas)

    assert isinstance(resultado, ResultadoParser)
    assert len(resultado.transiciones) == 10, f"Se esperaban 10 transiciones, hay {len(resultado.transiciones)}"
    assert "q0" in resultado.estados
    assert "qf" in resultado.estados
    assert "a" in resultado.simbolos
    assert "b" in resultado.simbolos
    assert "X" in resultado.simbolos
    assert "Y" in resultado.simbolos
    assert "B" in resultado.simbolos
    print("✓ Test Parser completado con exito.")


def test_cadena_aceptada_aabb_manual_match():
    """Valida la ejecucion exacta paso por paso contra la tabla manual del informe para 'aabb'."""
    ruta_reglas = Path(__file__).resolve().parent.parent / "src" / "ejemplos" / "an_bn_memoria.txt"
    resultado = parsear_archivo(ruta_reglas)
    motor = MaquinaTuringMemoria(resultado.transiciones)

    motor.iniciar("aabb")

    # Estados esperados segun la tabla de simulacion manual del informe
    esperados = [
        # (paso, estado, memoria, cinta_destacada, pos_cabezal)
        (0, "q0", MEMORIA_VACIA, "[a]abb", 0),
        (1, "q1", "a", "X[a]bb", 1),
        (2, "q1", "a", "Xa[b]b", 2),
        (3, "q1", MEMORIA_VACIA, "X[a]Yb", 1),
        (4, "q1", MEMORIA_VACIA, "[X]aYb", 0),
        (5, "q0", MEMORIA_VACIA, "X[a]Yb", 1),
        (6, "q1", "a", "XX[Y]b", 2),
        (7, "q1", "a", "XXY[b]", 3),
        (8, "q1", MEMORIA_VACIA, "XX[Y]Y", 2),
        (9, "q1", MEMORIA_VACIA, "X[X]YY", 1),
        (10, "q0", MEMORIA_VACIA, "XX[Y]Y", 2),
        (11, "q2", MEMORIA_VACIA, "XXY[Y]", 3),
        (12, "q2", MEMORIA_VACIA, "XXYY[B]", 4),
    ]

    for paso_idx, exp_estado, exp_mem, exp_cinta, exp_pos in esperados:
        cfg = motor.historial[paso_idx]
        assert cfg.paso == paso_idx, f"Paso {cfg.paso} != {paso_idx}"
        assert cfg.estado == exp_estado, f"Paso {paso_idx}: estado {cfg.estado} != {exp_estado}"
        assert cfg.memoria == exp_mem, f"Paso {paso_idx}: memoria {cfg.memoria} != {exp_mem}"
        assert cfg.representacion_cinta_destacada() == exp_cinta, (
            f"Paso {paso_idx}: cinta {cfg.representacion_cinta_destacada()} != {exp_cinta}"
        )
        assert cfg.posicion_cabezal == exp_pos, (
            f"Paso {paso_idx}: cabezal {cfg.posicion_cabezal} != {exp_pos}"
        )

        if paso_idx < len(esperados) - 1:
            continua = motor.paso()
            assert continua is True

    # El paso 12 debe haber alcanzado qf en el siguiente intento de avance o marcado aceptada
    assert motor.estado_actual == "q2"
    motor.paso() # Ejecuta q2, B, ε -> qf, B, R, ε
    cfg_final = motor.historial[-1]
    assert cfg_final.estado == "qf"
    assert cfg_final.memoria == MEMORIA_VACIA
    assert motor.estado_ejecucion == "ACEPTADA"
    print("✓ Test Cadena Aceptada 'aabb' coincide al 100% con la simulacion manual.")


def test_cadena_rechazada_aab():
    """Valida la ejecucion contra la tabla manual del informe para 'aab' (rechazada en paso 7)."""
    ruta_reglas = Path(__file__).resolve().parent.parent / "src" / "ejemplos" / "an_bn_memoria.txt"
    resultado = parsear_archivo(ruta_reglas)
    motor = MaquinaTuringMemoria(resultado.transiciones)

    motor.iniciar("aab")
    motor.ejecutar_todo()

    assert motor.estado_ejecucion == "RECHAZADA"
    # Debe detenerse con el cabezal en el blanco B (paso 7)
    cfg_parada = motor.historial[-1]
    assert cfg_parada.paso == 7
    assert cfg_parada.estado == "q1"
    assert cfg_parada.memoria == "a"
    assert cfg_parada.simbolo_leido == "B"
    assert cfg_parada.representacion_cinta_destacada() == "XXY[B]"
    print("✓ Test Cadena Rechazada 'aab' coincide exactamente con la especificacion.")


def test_varias_cadenas():
    ruta_reglas = Path(__file__).resolve().parent.parent / "src" / "ejemplos" / "an_bn_memoria.txt"
    resultado = parsear_archivo(ruta_reglas)

    aceptadas = ["ab", "aabb", "aaabbb", "aaaabbbb"]
    rechazadas = ["a", "b", "ba", "aab", "abb", "aabbab", "bbaa", "aaabb"]

    for cad in aceptadas:
        m = MaquinaTuringMemoria(resultado.transiciones)
        m.iniciar(cad)
        m.ejecutar_todo()
        assert m.estado_ejecucion == "ACEPTADA", f"Cadena '{cad}' deberia ser ACEPTADA, dio {m.estado_ejecucion}"

    for cad in rechazadas:
        m = MaquinaTuringMemoria(resultado.transiciones)
        m.iniciar(cad)
        m.ejecutar_todo()
        assert m.estado_ejecucion == "RECHAZADA", f"Cadena '{cad}' deberia ser RECHAZADA, dio {m.estado_ejecucion}"

    print(f"✓ Test {len(aceptadas)} cadenas aceptadas y {len(rechazadas)} rechazadas aprobado exitosamente.")


if __name__ == "__main__":
    test_parser()
    test_cadena_aceptada_aabb_manual_match()
    test_cadena_rechazada_aab()
    test_varias_cadenas()
    print("\nTODAS LAS PRUEBAS PASARON EXITOSAMENTE.")
