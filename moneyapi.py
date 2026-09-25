"""moneyapi.py：对外门面（老接口 set/add/mul 不能改）。"""
from __future__ import annotations

from fixedpoint import Fixed


class Amount:
    def __init__(self, decimals: int = 2):
        self.fixed = Fixed(decimals)

    def set(self, value) -> dict:
        return self.fixed.set(value)

    def add(self, other) -> "Amount":
        result = Amount(self.fixed.decimals)
        result.fixed = self.fixed.add(other.fixed if hasattr(other, "fixed") else other)
        return result

    def mul(self, other) -> "Amount":
        result = Amount(self.fixed.decimals)
        result.fixed = self.fixed.mul(other.fixed if hasattr(other, "fixed") else other)
        return result

    def set_rounding(self, mode: str) -> dict:
        return self.fixed.set_rounding(mode)

    def pack(self) -> bytes:
        return self.fixed.pack()

    def units(self) -> int:
        return self.fixed.to_units()
