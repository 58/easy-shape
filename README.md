# easy-shape
## Usage
1. `uv`をインストール
    https://github.com/astral-sh/uv
2. 以下のような配位構造のcsvを準備
    ```
    Fe,12.345678,90.123456,7.890123
    Br,45.678901,2.345678,9.012345
    Br,12.345678,90.123456,7.890123
    Br,23.456789,01.234567,8.901234
    Br,34.567890,12.345678,9.012345
    Br,45.678901,23.456789,0.123456
    Br,56.789012,34.567890,1.234567
    ```
3. `shape-measure`コマンドで測定
    `uv run shape-measure test.csv`
    `uv run shape-measure test.csv --ideal OC-6`
