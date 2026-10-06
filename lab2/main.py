from core.SolveResult import SolveResult
from core.ui import Parameter, App
from core.validators import Positive
from core.solver import runge_kutt


def find_k(t0: float, m0: float, half_life: float, step: float, epsilon: float) -> float:
    target_m = 0.5 * m0
    k_min, k_max = 0.000001, 0.01
    k_best = 0

    while (k_max - k_min) > epsilon:
        k_test = (k_max + k_min) / 2

        def current_f(t: float, x: float) -> float:
            return - k_test * x

        x_res, y_res = runge_kutt(current_f, t0, m0, half_life, step, epsilon)

        m = y_res[-1]

        if m < target_m:
            k_max = k_test
        else:
            k_min = k_test

        k_best = k_test

    return k_best


def solve(data: dict[str, float]) -> SolveResult:
    t0, m0, t_end, half_life, step, accuracy = data['t0'], data['m0'], data['t_end'], data['half_life'], data['step'], data['accuracy']
    epsilon = 10 ** int(accuracy)

    k = find_k(t0, m0, half_life, step, epsilon)

    def f(t: float, x: float) -> float:
        return - k * x

    t_list, x_list = runge_kutt(f, t0, m0, t_end, step, epsilon)

    return SolveResult(
        x_list=t_list,
        y_approximation=x_list,
        x_label='t (год)',
        y_label='x(t) (кг)',
    )


if __name__ == '__main__':
    params = [
        Parameter(key='t0', title='Начальное время (t0)', default='0', validators=[Positive(False)]),
        Parameter(key='m0', title='Начальная масса (m0)', default='100', validators=[Positive(True)]),
        Parameter(key='t_end', title='Конечное время (t_end)', default='200', validators=[Positive(True)]),
        Parameter(key='half_life', title='Период полураспада', default='1590', validators=[Positive(True)]),
    ]

    app = App(
        tittle='Лабораторная №2. Вариант 13. Ледовский Антон ИП1',
        lab_param_list=params,
        on_solve_callback=solve,
    )

    app.run()