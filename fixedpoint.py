"""fixedpoint.py：定点运算（基线：内部浮点）。"""
from __future__ import annotations


class Fixed:
    def __init__(self, decimals: int = 2):
        self.decimals = decimals
        self.value = 0.0
        self.rounding = "HALF_UP"

    def set(self, value) -> dict:
        """基线：直接存浮点。"""
        self.value = float(value)
        return {"value": self.value}

    def add(self, other) -> "Fixed":
        result = Fixed(self.decimals)
        result.value = self.value + other.value
        return result

    def mul(self, other) -> "Fixed":
        """基线：浮点相乘，不舍入。"""
        result = Fixed(self.decimals)
        result.value = self.value * other.value
        return result

    def to_units(self) -> int:
        raise NotImplementedError("定点整数还没实现")

    def pack(self) -> bytes:
        raise NotImplementedError("序列化还没实现")

    def max_error(self, exact) -> int:
        raise NotImplementedError("误差统计还没实现")

    def stats(self) -> dict:
        return {"decimals": self.decimals, "value": self.value, "rounding": self.rounding}
