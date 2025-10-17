# src/shape_measure/gui.py
from __future__ import annotations

import flet as ft
from pathlib import Path

from cosymlib import Geometry
# __init__.py で re-export している想定
from shape_measure import load_symbol_xyz, __version__


IDEAL_OPTIONS = [
    ("auto", "自動（OC-6 と TPR-6 を両方計算）"),
    ("OC-6", "OC-6"),
    ("TPR-6", "TPR-6"),
]


def main(page: ft.Page):
    page.title = f"Easy-Shape GUI v{__version__}"
    page.window_width = 760
    page.window_height = 540
    page.scroll = "auto"

    picked_path = ft.TextField(label="入力CSV（Element,x,y,z）", read_only=True, expand=True)
    central_atom = ft.TextField(label="中心原子インデックス（1始まり）", value="1", width=220)
    ideal = ft.Dropdown(
        label="理想構造",
        value="auto",
        options=[ft.dropdown.Option(k, text=v) for k, v in IDEAL_OPTIONS],
        width=320,
    )
    output = ft.Text(value="", selectable=True)

    file_picker = ft.FilePicker(
        on_result=lambda e: (
            setattr(picked_path, "value", e.files[0].path) if e.files else None,
            page.update()
        )
    )
    page.overlay.append(file_picker)
    page.update()

    def run_measure(_):
        output.value = ""
        page.update()

        if not picked_path.value:
            page.snack_bar = ft.SnackBar(ft.Text("CSV ファイルを選択してください。"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            ca = int(central_atom.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("中心原子インデックスは整数で指定してください。"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            structure, symbols = load_symbol_xyz(Path(picked_path.value))
            geom = Geometry(structure, symbols=symbols)

            if ideal.value == "auto":
                m_oc = geom.get_shape_measure("OC-6", central_atom=ca)
                m_tpr = geom.get_shape_measure("TPR-6", central_atom=ca)
                output.value = f"OC-6 measure: {m_oc:.3f}\nTPR-6 measure: {m_tpr:.3f}"
            else:
                m = geom.get_shape_measure(ideal.value, central_atom=ca)
                output.value = f"{ideal.value} measure: {m:.3f}"

        except Exception as e:
            output.value = f"エラー: {e}"

        page.update()

    pick_btn = ft.ElevatedButton(
        "CSVを選ぶ",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
    )
    run_btn = ft.FilledButton("計算する", icon=ft.Icons.PLAY_ARROW, on_click=run_measure)

    page.add(
        ft.Row([picked_path, pick_btn]),
        ft.Row([ideal, central_atom, run_btn], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        ft.Text("結果", weight=ft.FontWeight.BOLD),
        output,
    )


if __name__ == "__main__":
    # Flet ランタイムから起動
    ft.app(target=main, view=ft.AppView.FLET_APP)
