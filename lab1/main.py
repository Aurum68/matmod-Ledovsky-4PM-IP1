import math
from core.SolveResult import SolveResult
from core.solver import runge_kutt_boundary
from core.ui import Parameter, App
from core.validators import Positive, LessThan


def solve(data: dict[str, float]) -> SolveResult:
    t0, h0, r_bowl, r_hole, mu, step, accuracy = data['t0'], data['h0'], data['r_bowl'], data['r_hole'], data['mu'], \
    data['step'], data['accuracy']
    epsilon = 10 ** int(accuracy)

    def f(t: float, h: float, r_bowl: float = r_bowl, r_hole: float = r_hole, mu: float = mu) -> float:
        g = 9.8
        denominator = 2 * r_bowl * h - h ** 2
        if denominator <= 1e-8:
            return 0.0
        return - (mu * r_hole ** 2 * math.sqrt(2 * g * h)) / denominator

    g = 9.8
    t_analytic = (1.0 / (mu * (r_hole ** 2) * math.sqrt(2 * g))) * (
                (4.0 / 3.0) * r_bowl * (h0 ** 1.5) - 0.4 * (h0 ** 2.5))

    t_list, h_list, runge_err = runge_kutt_boundary(f, t0, h0, step, epsilon)

    result = SolveResult(
        x_list=t_list,
        y_approximation=h_list,
        x_label='t (секунды)',
        y_label='h(t) (метры)',
        info_text=(
            f"Аналитическое время: {t_analytic:.4f} с\n"
            f"Численное время: {t_list[-1]:.4f} с\n"
            f"Погрешность времени (Рунге): {runge_err:.2e}"
        )
    )

    return result


if __name__ == '__main__':
    params = [
        Parameter(key='t0', title='Начальное время (t0)', default='0', validators=[Positive(False)]),
        Parameter(key='h0', title='Начальный уровень воды в метрах (h0)', default='1',
                  validators=[Positive(True), LessThan('r_bowl', False)]),
        Parameter(key='r_bowl', title='Радиус чаши в метрах (R)', default='1', validators=[Positive(True)]),
        Parameter(key='r_hole', title='Радиус отверстия в метрах (r)', default='0.1',
                  validators=[Positive(True), LessThan('r_bowl', True)]),
        Parameter(key='mu', title='Коэффициент расхода жидкости (μ)', default='0.6', validators=[Positive(True)]),
    ]

    app = App(
        tittle='Лабораторная №1. Вариант 14. Ледовский Антон ИП1',
        lab_param_list=params,
        on_solve_callback=solve,
    )
    app.run()