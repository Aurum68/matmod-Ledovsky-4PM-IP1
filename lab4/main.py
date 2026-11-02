from core.SolveResult import SolveResult
from core.solver import finite_difference_method
from core.ui import Parameter, App
from core.validators import Positive


def solve(data: dict[str, float]) -> SolveResult:
    x0, y0, x1, y1, step, accuracy = data['x0'], data['y0'], data['x1'], data['y1'], data['step'], data['accuracy']
    epsilon = 10 ** int(accuracy)

    def f(x: float, y: float, dy: float) -> float:
        return - (dy ** 2 + 1) / (2 * y)

    t_list, x_list = finite_difference_method(f, x0, x1, y0, y1, step, epsilon)

    return SolveResult(
        x_list=t_list,
        y_approximation=x_list,
        x_label='x',
        y_label='y',
        invert_y=True,
    )


if __name__ == '__main__':
    params = [
        Parameter(key='x0', title='Начальная координата X (x0)', default='0', validators=[Positive(False)]),
        Parameter(key='y0', title='Начальная координата Y (y0)', default='0', validators=[Positive(False)]),
        Parameter(key='x1', title='Конечная координата X (x1)', default='4', validators=[Positive(False)]),
        Parameter(key='y1', title='Конечная координата Y (y1)', default='3', validators=[Positive(False)]),
    ]

    app = App(
        tittle='Лабораторная №4. Вариант 14. Ледовский Антон ИП1',
        lab_param_list=params,
        on_solve_callback=solve,
    )

    app.run()