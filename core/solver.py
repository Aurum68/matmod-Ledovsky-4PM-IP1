from typing import Callable
import numpy as np
from scipy.optimize import root

def __rk_compute(
        function: Callable[[float, float], float],
        x0: float,
        y0: float,
        x_end: float,
        step: float,
) -> tuple[list[float], list[float]]:
    x_list, y_list = [x0], [y0]
    x, y = x0, y0

    while x < x_end:
        k1 = function(x, y)
        k2 = function(x + step / 2, y + k1 * step / 2)
        k3 = function(x + step / 2, y + k2 * step / 2)
        k4 = function(x + step, y + k3 * step)

        y += step * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += step

        x_list.append(x)
        y_list.append(y)

    return x_list, y_list


def runge_kutt(
        function: Callable[[float, float], float],
        x0: float,
        y0: float,
        x_end: float,
        step: float,
        eps: float = 1e-6,
) -> tuple[list[float], list[float]]:
    x_prev, y_prev = __rk_compute(function, x0, y0, x_end, step)

    while True:
        step /= 2.0

        x_curr, y_curr = __rk_compute(function, x0, y0, x_end, step)

        err = abs(y_curr[-1] - y_prev[-1]) / 15.0

        if err < eps:
            return x_curr, y_curr

        y_prev = y_curr


def newton_tangent_method(
        function: Callable[[float], float],
        derivative: Callable[[float], float],
        x0: float,
        eps: float = 1e-6,
        max_iter: int = 100,
) -> float:
    xn = x0
    for _ in range(max_iter):
        der = derivative(xn)
        if abs(der) < 1e-12:
            raise RuntimeError

        x = xn - function(xn) / der
        if abs(xn - x) < eps:
            return x
        xn = x

    raise TimeoutError


def finite_difference_method(
        f: Callable[[float, float, float], float],
        x_start: float,
        x_end: float,
        y_start: float,
        y_end: float,
        step: float = 0.01,
        eps: float = 1e-6,
) -> tuple[np.ndarray, np.ndarray]:
    n_intervals = int(round((x_end - x_start) / step))
    n_points = n_intervals + 1

    x = np.linspace(x_start, x_end, n_points)
    h = x[1] - x[0]

    def system_of_equations(Y: np.ndarray) -> np.ndarray:
        residuals = np.zeros(n_points)
        residuals[0] = Y[0] - y_start
        residuals[-1] = Y[-1] - y_end

        for i in range(1, n_points - 1):
            dy = (Y[i + 1] - Y[i - 1]) / (2 * h)
            d2y = (Y[i + 1] - 2 * Y[i] + Y[i - 1]) / (h ** 2)
            f_val = f(x[i], Y[i], dy)
            residuals[i] = d2y - f_val

        return residuals

    Y_guess = np.linspace(y_start, y_end, n_points)

    solution = root(system_of_equations, Y_guess, tol=eps)

    if not solution.success:
        raise ValueError("Не удалось решить нелинейную систему. Попробуй другое начальное приближение.")

    return x, solution.x