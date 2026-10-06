"""Punto de entrada principal para el Simulador de Maquina de Turing con Memoria Interna Finita."""

import os
import sys

# Agregar la carpeta src al PYTHONPATH para imports limpios
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from interfaz.app import run_app

if __name__ == "__main__":
    run_app()
