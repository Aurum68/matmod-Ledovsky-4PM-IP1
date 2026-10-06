from typing import Callable


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
        eps: float,
) -> tuple[list[float], list[float]]:
    x_prev, y_prev = __rk_compute(function, x0, y0, x_end, step)

    while True:
        step /= 2.0

        x_curr, y_curr = __rk_compute(function, x0, y0, x_end, step)

        err = abs(y_curr[-1] - y_prev[-1]) / 15.0

        if err < eps:
            return x_curr, y_curr

        y_prev = y_curr