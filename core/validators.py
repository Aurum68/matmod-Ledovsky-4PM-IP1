from typing import Callable, Any


class ValidationError(Exception):
    def __init__(self, errors: dict[str, list[str]]):
        self.errors = errors
        super().__init__("Validation Error")


Validator = Callable[[Any, dict[str, Any]], str | None]


def Positive(strict: bool) -> Validator:
    def validator(x: float, values: dict[str, float]) -> str | None:
        ok = (x > 0) if strict else (x >= 0)
        return None if ok else "Значение должно быть " + ("> 0" if strict else ">= 0")
    return validator


def Interval(minimum: float, maximum: float, includes: bool) -> Validator:
    def validator(x: float, values: dict[str, float]) -> str | None:
        ok = (minimum <= x <= maximum) if includes else (minimum < x < maximum)
        return None if ok else f"Значение должно быть в диапазоне {minimum}..{maximum}"
    return validator


def GreaterThan(other_key: str, strict: bool) -> Validator:
    def validator(x: float, values: dict[str, float]) -> str | None:
        if other_key not in values:
            return None
        ok = (x > values[other_key]) if strict else (x >= values[other_key])
        return None if ok else "Значение должно быть " + (f"> {values[other_key]}" if strict else f">= {values[other_key]}")
    return validator