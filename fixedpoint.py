"""fixedpoint.py：定点运算（整数单位内核，仅用标准库）。"""
from __future__ import annotations

HALF_UP = "HALF_UP"
HALF_EVEN = "HALF_EVEN"
DOWN = "DOWN"

_MODES = (HALF_UP, HALF_EVEN, DOWN)
_SCALE = 8  # pack/unpack 使用 8 字节有符号整数


def _as_ratio(value) -> tuple[int, int]:
    """把输入值转成精确的正分母整数比 (num, den)。"""
    if isinstance(value, bool):
        return int(value), 1
    if isinstance(value, int):
        return value, 1
    if isinstance(value, float):
        return value.as_integer_ratio()
    if isinstance(value, str):
        text = value.strip()
        sign = 1
        if text[:1] in ("+", "-"):
            if text[0] == "-":
                sign = -1
            text = text[1:]
        whole, dot, frac = text.partition(".")
        if not whole:
            whole = "0"
        scale = 10 ** len(frac)
        num = int(whole) * scale + (int(frac) if frac else 0)
        return sign * num, scale
    raise TypeError(f"不支持的数值类型: {type(value).__name__}")


def _round_div(num: int, den: int, mode: str) -> int:
    """按指定模式对 num/den（den > 0）做整数舍入，全程整数运算。"""
    negative = num < 0
    q, r = divmod(abs(num), den)
    if r and mode != DOWN:
        twice = 2 * r
        if twice > den:
            q += 1
        elif twice == den:
            if mode == HALF_UP or (mode == HALF_EVEN and q % 2 == 1):
                q += 1
    return -q if negative else q


class Fixed:
    def __init__(self, decimals: int = 2):
        self.decimals = int(decimals)
        self.value = 0.0
        self.rounding = HALF_UP
        self._num = 0
        self._den = 1

    def set(self, value) -> dict:
        """存成定点：保留精确整数比，取单位时按当前舍入模式 round(value*10^decimals)。"""
        self._num, self._den = _as_ratio(value)
        self.value = float(value)
        return {"value": self.value}

    def set_rounding(self, mode: str) -> dict:
        if mode not in _MODES:
            raise ValueError(f"未知舍入模式: {mode!r}")
        self.rounding = mode
        return {"rounding": mode}

    def to_units(self) -> int:
        """定点整数单位 = round(value × 10^decimals)，按当前舍入模式。"""
        return _round_div(self._num * (10 ** self.decimals), self._den, self.rounding)

    def add(self, other) -> "Fixed":
        return self._combine(other, subtract=False)

    def sub(self, other) -> "Fixed":
        return self._combine(other, subtract=True)

    def _combine(self, other: "Fixed", subtract: bool) -> "Fixed":
        decimals = max(self.decimals, other.decimals)
        left = self.to_units() * (10 ** (decimals - self.decimals))
        right = other.to_units() * (10 ** (decimals - other.decimals))
        return self._from_units(left - right if subtract else left + right, decimals)

    def mul(self, other) -> "Fixed":
        """乘积按最低位归一：u1*u2 放大了 10^(d1+d2)，归一回目标小数位。"""
        decimals = self.decimals
        scaled = self.to_units() * other.to_units() * (10 ** decimals)
        units = _round_div(scaled, 10 ** (self.decimals + other.decimals), self.rounding)
        return self._from_units(units, decimals)

    def _from_units(self, units: int, decimals: int) -> "Fixed":
        result = Fixed(decimals)
        result.rounding = self.rounding
        result._num = units
        result._den = 10 ** decimals
        result.value = units / result._den
        return result

    def pack(self) -> bytes:
        """序列化为 8 字节大端有符号整数。"""
        return self.to_units().to_bytes(_SCALE, byteorder="big", signed=True)

    def unpack(self, blob) -> dict:
        """从 8 字节大端有符号整数还原，并写回当前对象。"""
        units = int.from_bytes(blob, byteorder="big", signed=True)
        self._num = units
        self._den = 10 ** self.decimals
        self.value = units / self._den
        return {"units": units, "value": self.value}

    def max_error(self, exact) -> int:
        """与精确值之差（最小单位计）：精确值按同一模式量化后与本定点之差。"""
        num, den = _as_ratio(exact)
        target = _round_div(num * (10 ** self.decimals), den, self.rounding)
        return abs(self.to_units() - target)

    def stats(self) -> dict:
        return {
            "decimals": self.decimals,
            "value": self.value,
            "rounding": self.rounding,
            "units": self.to_units(),
        }
