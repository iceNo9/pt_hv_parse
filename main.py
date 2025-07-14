import importlib.metadata
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from typing import Dict, List

from pt_hv_parse.delta_decoder import DeltaDecoder
from pt_hv_parse.parser import DevPidParser
from pt_hv_parse.plot_util import plot_interactive, write_csv


def parse_data_from_file(file_path: str) -> List[Dict[str, int]]:
    """
    假设输入文件是 JSON 格式的字典数组：
    [{"x":0,"y":1000}, {"x":1,"y":1050}, ...]
    你可以根据需求改这里的解析逻辑
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 简单校验
        for d in data:
            if not isinstance(d, dict) or "x" not in d or "y" not in d:
                raise ValueError("数据格式错误，必须为包含 x 和 y 的字典")
        return data
    except Exception as e:
        raise e


UI_VERSION = "0.1.0"


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("高压PID数据解析器")
        self.root.geometry("700x400")

        # 输入路径
        self.path_label = tk.Label(root, text="输入文件路径:")
        self.path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(root, textvariable=self.path_var, width=60)
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.open_btn = tk.Button(root, text="打开文件", command=self.open_file)
        self.open_btn.grid(row=0, column=2, padx=5, pady=5)

        # 解析按钮
        self.parse_btn = tk.Button(root, text="解析", command=self.parse_and_generate)
        self.parse_btn.grid(row=1, column=1, pady=10)

        # 日志框
        self.log_text = scrolledtext.ScrolledText(root, width=85, height=15)
        self.log_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # === 左下角版本信息 ===
        try:
            core_version = importlib.metadata.version("pt_hv_parse")
        except importlib.metadata.PackageNotFoundError:
            core_version = "未知"

        version_frame = tk.Frame(root)
        version_frame.grid(row=3, column=0, sticky="w", padx=10, pady=(0, 5))

        tk.Label(version_frame, text=f"内核版本: {core_version}", anchor="w", fg="gray").pack(anchor="w")
        tk.Label(version_frame, text=f"UI版本: {UI_VERSION}", anchor="w", fg="gray").pack(anchor="w")

    def log(self, msg: str) -> None:
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="选择数据文件", filetypes=[("日志文件", "*.log *.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.path_var.set(file_path)
            self.log(f"选中文件: {file_path}")

    def parse_and_generate(self) -> None:
        input_path = self.path_var.get().strip()
        if not input_path or not os.path.isfile(input_path):
            messagebox.showerror("错误", "请输入有效的文件路径")
            return

        try:
            self.log("开始解析输入数据...")
            parser = DevPidParser(input_path)
            data_dict = parser.parse()
            self.log(f"解析到 {len(data_dict.get('pids', []))} 条 PID 数据")

            # 使用 DeltaDecoder 解码
            decoder = DeltaDecoder()
            decoded_data = decoder.decode_all(data_dict)

            # 输出文件名，和输入同目录
            base_dir = os.path.dirname(input_path)
            csv_path = os.path.join(base_dir, "output_data.csv")
            html_path = os.path.join(base_dir, "interactive_plot.html")

            self.log("开始写入 CSV 文件...")
            write_csv(decoded_data["combined"], csv_path)
            self.log(f"CSV 文件已写入: {csv_path}")

            self.log("开始生成交互式图表...")
            plot_interactive(decoded_data["combined"], html_path)
            self.log(f"交互式图表已生成: {html_path}")

            messagebox.showinfo("完成", "CSV和图表生成成功！")

        except Exception as e:
            self.log(f"错误: {e}")
            messagebox.showerror("错误", f"解析或生成失败:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
