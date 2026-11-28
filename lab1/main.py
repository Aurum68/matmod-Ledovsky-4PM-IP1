import math

from core.SolveResult import SolveResult
from core.solver import runge_kutt
from core.ui import Parameter, App
from core.validators import Positive, LessThan, Interval


def solve(data: dict[str, float]) -> SolveResult:
    t0, h0, r_bowl, r_hole, mu, step, accuracy = data['t0'], data['h0'], data['r_bowl'], data['r_hole'], data['mu'], data['step'], data['accuracy']
    epsilon = 10 ** int(accuracy)

    def f(
            t: float,
            h: float,
            r_bowl: float = r_bowl,
            r_hole: float = r_hole,
            mu: float = mu,
    ) -> float:
        if h <= 1e-8:
            return 0.0

        g = 9.8
        denominator = 2 * r_bowl * h - h ** 2
        if denominator <= 1e-8:
            return 0.0
        return - (mu * r_hole ** 2 * math.sqrt(2 * g * h)) / (2 * r_bowl * h - h ** 2)

    def check_empty(t: float, h: float) -> bool:
        return h <= 1e-8

    t_list, h_list = runge_kutt(f, t0, h0, 1000, step, epsilon, check_empty)

    return SolveResult(
        x_list=t_list,
        y_approximation=h_list,
        x_label='t (секунды)',
        y_label='h(t) (метры)',
        info_text=f'Время опорожнения бака {t_list[-1]:4f} секунд'
    )


if __name__ == '__main__':
    params = [
        Parameter(key='t0', title='Начальное время (t0)', default='0', validators=[Positive(False)]),
        Parameter(key='h0', title='Начальный уровень воды в метрах (h0)', default='1', validators=[Positive(True), LessThan('r_bowl', False)]),
        Parameter(key='r_bowl', title='Радиус чаши в метрах (R)', default='1', validators=[Positive(True)]),
        Parameter(key='r_hole', title='Радиус отверстия в метрах (r)', default='0.1', validators=[Positive(True),LessThan('r_bowl', True)]),
        Parameter(key='mu', title='Коэффициент расхода жидкости (μ)', default='0.6', validators=[Positive(True)]),
    ]

    app = App(
        tittle='Лабораторная №1. Вариант 14. Ледовский Антон ИП1',
        lab_param_list=params,
        on_solve_callback=solve,
    )

    app.run()