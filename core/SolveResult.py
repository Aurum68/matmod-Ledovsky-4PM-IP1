from dataclasses import dataclass
from typing import List


@dataclass
class SolveResult:
    x_list: List[float]
    y_approximation: List[float]

    x_label: str = "x"
    y_label: str = "y"
    approx_legend: str = "Приближённое решение"