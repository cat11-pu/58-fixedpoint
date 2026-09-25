# fixedpoint

纯 Python 标准库的定点运算内核（内部为整数单位，不使用 decimal/Fraction/浮点累加）。

## 用法

```python
from fixedpoint import Fixed

a = Fixed(decimals=2)          # 2 位小数，内部单位 = value * 100
a.set(1.125)                   # {"value": 1.125}，按当前舍入模式量化
b = Fixed(2)
b.set(2.25)

a.add(b).to_units()            # 338（同小数位直接按整数单位相加）
a.mul(b).to_units()            # 254（乘积按最低位归一）

a.set_rounding("HALF_EVEN")    # HALF_UP / HALF_EVEN / DOWN
a.to_units()                   # 112
blob = a.pack()                # 8 字节大端有符号整数
Fixed(2).unpack(blob)          # {"units": 112, "value": 1.12}，往返一致
a.max_error(1.125)             # 与精确值之差（最小单位计，0 表示无误差）
```

`moneyapi.Amount` 是对外门面，`set/add/mul` 的返回结构保持兼容。

## 测试

    python3 -m unittest discover -s tests -v

## 场景自检

    python3 check_sample.py
