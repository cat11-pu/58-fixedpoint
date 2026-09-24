"""check_sample.py：按 sample/ops.json 走一圈，打印验收面。"""
import json
import os
import sys

from fixedpoint import Fixed


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "ops.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)
    left = Fixed(spec["decimals"])
    left.set(spec["left"])
    right = Fixed(spec["decimals"])
    right.set(spec["right"])
    total = left.add(right)
    product = left.mul(right)
    rounded = {}
    for mode in spec["modes"]:
        item = Fixed(spec["decimals"])
        item.set(spec["left"])
        item.rounding = mode
        rounded[mode] = item.to_units()
    blob = total.pack()
    reborn = Fixed(spec["decimals"])
    restored = reborn.unpack(blob)
    error = total.max_error(spec["exact_total"])
    print("加法结果的定点整数 =", total.to_units())
    print("乘法结果的定点整数 =", product.to_units())
    print("各舍入模式下的定点整数 =", rounded)
    print("序列化（hex） =", blob.hex())
    print("反序列化后的定点整数 =", restored.get("units"))
    print("与精确值的最大误差（最小单位） =", error)
    print("误差上界（最小单位） =", spec["error_limit"])
    print("不变量（序列化往返一致） =", spec["roundtrip_invariant"])
    print("小数位数 =", spec["decimals"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
