import random
import time
import os

# --- 1. CONFIGURACIÓN DEL JUEGO ---
FILAS = 6
COLUMNAS = 10
VACIO = '.'
BLOQUE = 'X'

# Definición de las 7 piezas (Tetrominos).
# Las coordenadas son relativas a un punto de pivote (0, 0).
TETROMINOS = [
    # I
    [(-1, 0), (0, 0), (1, 0), (2, 0)],
    # O
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    # T
    [(-1, 0), (0, -1), (0, 0), (0, 1)],
    # L
    [(-1, 0Entiendo. Quieres la **lógica básica del Tetris** ejecutándose directamente en la consola (terminal), utilizando solo caracteres de texto, sin ninguna biblioteca gráfica como Pygame ni colores.

Aquí tienes un código Python que simula la caída, movimiento horizontal y fijación de una pieza en un tablero simple de $10 \times 20$ (el tamaño estándar, ya que $10 \times 6$ es demasiado pequeño).

## 🐍 Tetris Mínimo en Consola (Python)

Este código utiliza la función `time.sleep()` para simular la caída temporal y requiere que ejecutes el archivo directamente en tu terminal.

```python
import time
import random

# --- 1. Configuración del Tablero ---
FILAS = 20
COLUMNAS = 10
VACIO = '.'
BORDE = '#' # Carácter para representar los bloques fijos

# --- 2. Definición de Piezas ---
# Solo usamos la pieza 'I