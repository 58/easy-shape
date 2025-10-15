# src/shape_measure/cli.py
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import List, Tuple

from cosymlib import Geometry


def load_symbol_xyz(path: str | Path) -> Tuple[List[List[float]], List[str]]:
    """
    Element,x,y,z 形式のCSV/テキストを読み込み、
    structure (List[List[float]]) と symbols (List[str]) を返す。

    仕様:
      - 区切りはカンマを想定
      - 空行と '#' 始まりのコメント行はスキップ
      - 例行: Fe,12.345678,90.123456,78.901234
    """
    path = Path(path)
    structure: List[List[float]] = []
    symbols: List[str] = []

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            if row[0].strip().startswith("#"):
                continue
            if len(row) < 4:
                raise ValueError(f"列数が不足しています: {row}")

            sym = row[0].strip()
            try:
                x, y, z = map(float, row[1:4])
            except ValueError as e:
                raise ValueError(f"数値に変換できません: {row}") from e

            symbols.append(sym)
            structure.append([x, y, z])

    return structure, symbols


def main() -> None:
    p = argparse.ArgumentParser(
        description="Continuous shape measure (cosymlib) — CSVから座標を読み込み実行します。"
    )
    p.add_argument(
        "input",
        help="入力CSVファイルパス（Element,x,y,z 形式）",
    )
    p.add_argument(
        "--ideal",
        default="0",
        help="理想構造ラベル（例: OC-6, TPR-6 など）",
    )
    p.add_argument(
        "--central-atom",
        type=int,
        default=1,
        dest="central_atom",
        help="中心原子のインデックス（0始まり、例: 先頭が中心なら 0）",
    )
    args = p.parse_args()

    structure, symbols = load_symbol_xyz(args.input)
    geom = Geometry(structure, symbols=symbols)
    
    if args.ideal == "0":
        measure_oc = geom.get_shape_measure("OC-6", central_atom=args.central_atom)
        measure_tpr = geom.get_shape_measure("TPR-6", central_atom=args.central_atom)

        print(f"OC-6 measure: {measure_oc:.3f}")
        print(f"TPR-6 measure: {measure_tpr:.3f}")
    else:
        measure = geom.get_shape_measure(args.ideal, central_atom=args.central_atom)
        print(f"{args.ideal} measure: {measure:.3f}")

if __name__ == "__main__":
    main()
