# lcg_unix.py
# Generador congruencial lineal (parámetros de Unix)
# x_{n+1} = (1103515245 * x_n + 12345) mod 2^32

import math
import argparse
import csv
from math import gcd

# --- PDF (matplotlib) ---
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

A = 1103515245
C = 12345
M = 2**32  # 4294967296


def lcg_unix(seed: int, n: int, a: int = A, c: int = C, m: int = M):
    """Devuelve una lista con n números enteros del LCG (parámetros de Unix)."""
    x = seed % m
    out = []
    for _ in range(n):
        x = (a * x + c) % m
        out.append(int(x))
    return out


# --------- Período (Hull–Dobell) ----------
def prime_factors(n: int):
    """Factores primos sin repetición."""
    fac = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            fac.add(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2  # probar 2 y luego solo impares
    if n > 1:
        fac.add(n)
    return fac


def has_full_period(a: int, c: int, m: int) -> bool:
    """
    Hull–Dobell:
      1) gcd(c, m) = 1
      2) a-1 es múltiplo de todos los primos de m
      3) Si m es múltiplo de 4, entonces a-1 es múltiplo de 4
    """
    if gcd(c, m) != 1:
        return False
    primes_m = prime_factors(m)
    for p in primes_m:
        if (a - 1) % p != 0:
            return False
    if m % 4 == 0 and (a - 1) % 4 != 0:
        return False
    return True


# --------- Guardar PDF bonito ----------
def save_pdf(numbers, seed: int, pdf_path: str, a: int = A, c: int = C, m: int = M):
    """
    Crea un PDF con:
      - Portada (fórmula, parámetros, período teórico)
      - Páginas con los números en cuadricula (4 columnas)
    """
    pp = PdfPages(pdf_path)

    # Portada
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis("off")
    cover_text = (
        "Generador Congruencial Lineal (parámetros de Unix)\n\n"
        r"$x_{n+1} = (1103515245 \cdot x_n + 12345)\ \mathrm{mod}\ 2^{32}$" "\n\n"
        f"Semilla (x0): {seed}\n"
        f"a = {a}\n"
        f"c = {c}\n"
        f"m = 2^32 = {m:,}\n\n"
        f"¿Cumple período completo por Hull–Dobell?: {'Sí' if has_full_period(a,c,m) else 'No'}\n"
        f"Período teórico: {m:,}\n\n"
        "Este documento contiene los primeros 1,000 números enteros generados."
    )
    ax.text(0.5, 0.5, cover_text, ha="center", va="center",
            fontsize=14, family="monospace", wrap=True)
    pp.savefig(fig)
    plt.close(fig)

    # Páginas con números (4 columnas x 60 filas = 240 por página)
    numbers_per_page = 240
    cols = 4
    rows = numbers_per_page // cols
    total = len(numbers)
    pages = math.ceil(total / numbers_per_page)

    for p in range(pages):
        start = p * numbers_per_page
        end = min((p + 1) * numbers_per_page, total)
        subset = numbers[start:end]

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        ax.text(0.5, 0.97, f"Números aleatorios (página {p+1} de {pages})",
                ha="center", va="top", fontsize=12)

        left_margin = 0.08
        right_margin = 0.92
        top = 0.92
        bottom = 0.06

        col_width = (right_margin - left_margin) / cols
        usable_height = (top - bottom)
        row_step = usable_height / rows

        for i, val in enumerate(subset):
            cidx = i // rows
            ridx = i % rows
            if cidx >= cols:
                continue
            x_pos = left_margin + cidx * col_width
            y_pos = top - ridx * row_step
            ax.text(x_pos, y_pos, f"{start + i + 1:>4}: {val}",
                    ha="left", va="top", fontsize=9, family="monospace")

        pp.savefig(fig)
        plt.close(fig)

    pp.close()


def save_csv(numbers, csv_path: str):
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "x_n"])
        for i, v in enumerate(numbers, start=1):
            w.writerow([i, v])


def main():
    parser = argparse.ArgumentParser(
        description="Generador LCG (Unix) y exportación a PDF/CSV."
    )
    parser.add_argument("--seed", type=int, default=111, help="Semilla x0 (por defecto 111)")
    parser.add_argument("--count", type=int, default=1000, help="Cantidad de números a generar (por defecto 1000)")
    parser.add_argument("--out", type=str, default="LCG_Unix",
                        help="Prefijo de salida (PDF/CSV), por defecto 'LCG_Unix'")
    args = parser.parse_args()

    nums = lcg_unix(args.seed, args.count)

    # Mostrar un resumen por consola
    print("=== Resumen ===")
    print(f"Fórmula: x_(n+1) = (1103515245*x_n + 12345) mod 2^32")
    print(f"Semilla: {args.seed}")
    print(f"Período teórico (si cumple Hull–Dobell): {M:,}")
    print(f"¿Cumple período completo?: {'Sí' if has_full_period(A,C,M) else 'No'}\n")
    print("Primeros 10 valores:", nums[:10])

    # Guardar archivos
    pdf_path = f"{args.out}_1000.pdf"
    csv_path = f"{args.out}_1000.csv"
    save_pdf(nums, args.seed, pdf_path)
    save_csv(nums, csv_path)

    print(f"\nArchivos guardados:")
    print(f" - PDF: {pdf_path}")
    print(f" - CSV: {csv_path}")
    print("\nRichard Chavez Cano")

if __name__ == "__main__":
    main()