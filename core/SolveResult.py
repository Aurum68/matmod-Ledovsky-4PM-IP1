from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class SolveResult:
    x_list: List[float]|np.ndarray
    y_approximation: List[float]|np.ndarray

    x_label: str = "x"
    y_label: str = "y"
    approx_legend: str = "Приближённое решение"

    invert_y: bool = False