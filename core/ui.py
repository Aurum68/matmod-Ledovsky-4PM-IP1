import tkinter as tk
from dataclasses import dataclass, field
from tkinter import Text, Toplevel, Label, messagebox, ttk
from typing import Any, Callable

import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from core.SolveResult import SolveResult
from core.validators import Validator, ValidationError, Positive


class Tooltip:
    def __init__(self, widget: Text, text: str) -> None:
        self.widget: Text = widget
        self.text: str = text
        self.tooltip_window: Toplevel | None = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event: tk.Event | None = None) -> None:
        if self.tooltip_window is not None:
            return

        x: int = self.widget.winfo_rootx() + 20  # Позиция всплывающего окна
        y: int = self.widget.winfo_rooty() + 20
        self.tooltip_window = Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Отключаем заголовок окна
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label: Label = Label(self.tooltip_window, text=self.text, bg="yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event: tk.Event | None = None) -> None:
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


@dataclass
class Parameter:
    key: str
    title: str
    default: str = ''
    validators: list[Validator] = field(default_factory=list)
    entry: tk.Entry | None = None
    var: tk.StringVar | None = None

    def build(self, root: tk.Tk, row: int, vcmd: tuple[str, str]) -> None:
        self.var = tk.StringVar(value=self.default)
        tk.Label(root, text=self.title).grid(row=row, column=0)
        self.entry = tk.Entry(root, textvariable=self.var, width=30, validate='key', validatecommand=vcmd)
        self.entry.grid(row=row, column=1)

    def read(self) -> Any:
        assert self.var.get() is not None
        value = self.var.get().strip()
        return float(value)


@dataclass
class Form:
    parameters: list[Parameter]

    def build(self, root: tk.Tk, vcmd: tuple[str, str]) -> None:
        for r, p in enumerate(self.parameters):
            p.build(root, r, vcmd)

    def validate(self) -> dict[str, float]:
        errors: dict[str, list[str]] = {}
        values: dict[str, float] = {}

        for p in self.parameters:
            try:
                values[p.key] = p.read()
            except Exception:
                errors.setdefault(p.key, []).append('Значение должно быть числом')

        for p in self.parameters:
            if p.key not in values:
                continue
            for v in p.validators:
                msg = v(values[p.key], values)
                if msg:
                    errors.setdefault(p.key, []).append(msg)

        if errors:
            raise ValidationError(errors)

        return values

    def show_error(self, err: ValidationError) -> None:
        for p in self.parameters:
            if p.entry is None:
                continue
            p.entry.config(bg=("misty rose" if p.key in err.errors else "white"))

        lines = []
        for p in self.parameters:
            if p.key in err.errors:
                for msg in err.errors[p.key]:
                    lines.append(f'{p.title}: {msg}')

        messagebox.showerror("Error", "\n".join(lines))


def only_float(P: str) -> bool:
    if P in ('', '-', '.'):
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False



class App:
    def __init__(self,
                 tittle: str,
                 lab_param_list: list[Parameter],
                 on_solve_callback: Callable[[dict[str, float]], SolveResult],
            ) -> None:
        self.root = tk.Tk()
        self.root.title(tittle)

        vcmd = (self.root.register(only_float), '%P')
        base_params: list[Parameter] = [
            Parameter(key='step', title='Шаг сетки', default='0.01', validators=[Positive(True)]),
            Parameter(key='accuracy', title='Точность вычислений (показатель)', default='-6', validators=[]),
        ]

        self.form: Form = Form(parameters=lab_param_list + base_params)
        self.form.build(self.root, vcmd)

        self.on_solve_callback = on_solve_callback

        tk.Button(self.root, text='Рассчитать', command=self.__on_click_solve).grid(row=len(self.form.parameters), column=0, columnspan=2, padx=10, pady=10)

        self.tree = ttk.Treeview(self.root, columns=('x', 'y'), show='headings')
        self.tree.grid(column=2, row=0, rowspan=10)

        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)


    def __on_click_solve(self) -> None:
        try:
            data = self.form.validate()

            result = self.on_solve_callback(data)

            accuracy = int(data.get('accuracy', -6))

            self.__draw_table(result, accuracy)
            self.__draw_graphics(result)

        except ValidationError as e:
            self.form.show_error(e)


    def __draw_table(self, result: SolveResult, accuracy: int) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.tree.heading('x', text=result.x_label)
        self.tree.heading('y', text=result.y_label)

        for i in range(len(result.x_list)):
            self.tree.insert('', 'end', values=(round(result.x_list[i], -accuracy), round(result.y_approximation[i], -accuracy)))


    def __draw_graphics(self, result: SolveResult) -> None:
        self.ax.clear()

        x_np, y_np = numpy.array(result.x_list), numpy.array(result.y_approximation)

        self.ax.grid(True)

        self.ax.plot(x_np, y_np, label=result.approx_legend, color='blue', linewidth=0.5)

        self.ax.legend()
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=2, row=10)


    def run(self) -> None:
        self.root.mainloop()
