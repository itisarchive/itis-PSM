import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


def build_system(n: int,
                 t_top: float,
                 t_bottom: float,
                 t_left: float,
                 t_right: float):
    a = lil_matrix((n * n, n * n), dtype=np.float64)
    b = np.zeros(n * n, dtype=np.float64)
    for row in range(n):
        for col in range(n):
            idx = row * n + col
            a[idx, idx] = -4.0
            if col > 0:
                a[idx, idx - 1] = 1.0
            else:
                b[idx] -= t_left
            if col < n - 1:
                a[idx, idx + 1] = 1.0
            else:
                b[idx] -= t_right
            if row > 0:
                a[idx, idx - n] = 1.0
            else:
                b[idx] -= t_bottom
            if row < n - 1:
                a[idx, idx + n] = 1.0
            else:
                b[idx] -= t_top
    return a.tocsr(), b


def solve_plate(n: int,
                t_top: float,
                t_bottom: float,
                t_left: float,
                t_right: float):
    a, b = build_system(n, t_top, t_bottom, t_left, t_right)
    x = spsolve(a, b)
    return x.reshape((n, n))[::-1]


def add_boundaries(field: np.ndarray,
                   t_top: float,
                   t_bottom: float,
                   t_left: float,
                   t_right: float):
    n = field.shape[0]
    full = np.empty((n + 2, n + 2))
    full[1:-1, 1:-1] = field
    full[0, 1:-1] = t_top
    full[-1, 1:-1] = t_bottom
    full[1:-1, 0] = t_left
    full[1:-1, -1] = t_right
    full[0, 0] = (t_top + t_left) / 2
    full[0, -1] = (t_top + t_right) / 2
    full[-1, 0] = (t_bottom + t_left) / 2
    full[-1, -1] = (t_bottom + t_right) / 2
    return full


def plot_field(field: np.ndarray):
    plt.imshow(field, cmap="jet")
    plt.colorbar(label="Temperatura [°C]")
    plt.savefig("labo04.png", dpi=300)
    plt.show()


def main():
    n = 40
    t_top = 50.0
    t_bottom = -20.0
    t_left = -50.0
    t_right = 20.0
    interior = solve_plate(n, t_top, t_bottom, t_left, t_right)
    full = add_boundaries(interior, t_top, t_bottom, t_left, t_right)
    plot_field(full)


if __name__ == "__main__":
    main()
