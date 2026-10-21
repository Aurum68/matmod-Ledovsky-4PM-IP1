from core.SolveResult import SolveResult
from core.solver import runge_kutt
from core.ui import Parameter, App
from core.validators import Positive


def solve(data: dict[str, float]) -> SolveResult:
    t0, x0, t_end, step, accuracy = data['t0'], data['x0'], data['t_end'], data['step'], data['accuracy']
    epsilon = 10 ** int(accuracy)

    def f(t: float, x: float) -> float:
        return (1 - x) / 3

    t_list, x_list = runge_kutt(f, t0, x0, t_end, step, epsilon)

    return SolveResult(
        x_list=t_list,
        y_approximation=x_list,
        x_label='t (год)',
        y_label='x(t) (доля)',
    )


if __name__ == '__main__':
    params = [
        Parameter(key='t0', title='Начальное время (t0)', default='0', validators=[Positive(False)]),
        Parameter(key='x0', title='Начальная доля переболевших (x0)', default='0', validators=[Positive(False)]),
        Parameter(key='t_end', title='Конечное время (t_end)', default='7', validators=[Positive(True)]),
    ]

    app = App(
        tittle='Лабораторная №3. Вариант 14. Ледовский Антон ИП1',
        lab_param_list=params,
        on_solve_callback=solve,
    )

    app.run()