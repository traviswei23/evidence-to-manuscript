"""从原始重复读数独立复算两组均值；不推断统计显著性。"""

import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


def means_from_csv(source, left, right):
    if left == right:
        raise ValueError("请选择两个不同的组。")
    values = {name: [] for name in (left, right)}
    units = set()
    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if len(reader.fieldnames or []) != len(set(reader.fieldnames or [])):
            raise ValueError("表头包含重复列名。")
        if not {"group", "value", "unit"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV 需要 group、value、unit 三列。")
        for row in reader:
            group = (row["group"] or "").strip()
            if group not in values:
                continue
            unit = (row["unit"] or "").strip()
            try:
                value = Decimal((row["value"] or "").strip())
            except InvalidOperation as exc:
                raise ValueError(f"第 {reader.line_num} 行没有可核查的数值。") from exc
            if not value.is_finite() or not unit:
                raise ValueError(f"第 {reader.line_num} 行的数值或单位不完整。")
            units.add(unit)
            values[group].append(value)
    if not all(values.values()):
        raise ValueError("至少有一个指定组在 CSV 中没有读数。")
    if len(units) != 1:
        raise ValueError("检测到不同单位，请先核实并显式换算。")
    avg = {key: sum(series) / len(series) for key, series in values.items()}
    delta = avg[left] - avg[right]
    relative = None if avg[right] == 0 else delta * 100 / avg[right]
    return {
        "left": left,
        "right_reference": right,
        "unit": units.pop(),
        "n_readings": {key: len(series) for key, series in values.items()},
        "means": {key: str(value) for key, value in avg.items()},
        "left_minus_right": str(delta),
        "relative_change_percent": None if relative is None else str(relative),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--left", required=True)
    parser.add_argument("--right", required=True, help="相对变化的基准组")
    args = parser.parse_args()
    try:
        result = means_from_csv(args.csv, args.left, args.right)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        parser.exit(2, f"无法复算：{exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

