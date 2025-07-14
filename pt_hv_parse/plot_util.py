import csv
from typing import Dict, List

from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file, save


def write_csv(data_points: List[Dict[str, int]], csv_path: str) -> None:
    """根据字典列表写入 CSV，列名为 X, Y"""
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["X", "Y"])
        writer.writeheader()
        for point in data_points:
            writer.writerow({"X": point["x"], "Y": point["y"]})
    print(f"✅ CSV 文件已写入: {csv_path}")


def plot_interactive(data_points: List[Dict[str, int]], html_path: str) -> None:
    """使用 Bokeh 根据数据生成交互式曲线图，并保存 HTML 文件"""
    x_vals = [p["x"] for p in data_points]
    y_vals = [p["y"] for p in data_points]
    labels = [f"({x},{y})" for x, y in zip(x_vals, y_vals)]

    source = ColumnDataSource(data=dict(x=x_vals, y=y_vals, label=labels))

    output_file(html_path, title="Vol over Time")

    p = figure(
        title="Vol over Time",
        x_axis_label="X",
        y_axis_label="Y",
        tooltips="@label",
        sizing_mode="stretch_width",
        height=400,
    )

    p.line("x", "y", source=source, line_width=3)
    p.circle("x", "y", source=source, size=10, color="blue")

    save(p)
    print(f"✅ 交互式图表已保存: {html_path}")


if __name__ == "__main__":
    test_data = [
        {"x": 0, "y": 1000},
        {"x": 1, "y": 1050},
        {"x": 2, "y": 1100},
        {"x": 3, "y": 950},
        {"x": 4, "y": 970},
    ]

    csv_file = "output_data.csv"
    html_file = "interactive_plot.html"

    write_csv(test_data, csv_file)
    plot_interactive(test_data, html_file)
