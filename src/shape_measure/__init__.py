"""
shape_measure パッケージの公開API。

- load_symbol_xyz(path): Element,x,y,z 形式のファイルを読み込み、
  (structure, symbols) を返す。
"""

from __future__ import annotations

# CLI 実装にあるユーティリティを公開する
from .cli import load_symbol_xyz  # re-export

__all__: list[str] = ["load_symbol_xyz", "__version__"]
__version__ = "0.1.0"
