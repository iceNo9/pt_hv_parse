import os
import subprocess
import sys
import zipfile


def run_nuitka(project_dir):
    entry_file = os.path.join(project_dir, "main.py")
    output_dir = os.path.join(project_dir, "dist")
    project_name = os.path.basename(project_dir)
    target_exe_name = f"{project_name}.exe"

    # Nuitka 编译命令
    nuitka_cmd = [
        "nuitka",
        "--standalone",
        "--windows-console-mode=disable",
        "--enable-plugin=tk-inter",
        "--output-dir=%s" % output_dir,
        entry_file,
    ]

    cmd = ["poetry", "run"] + nuitka_cmd

    print(f"开始用 Poetry 虚拟环境打包 {entry_file} ...")

    # ✅ 使用 sys.stdout/stderr 保留进度条、彩色输出等
    process = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return_code = process.wait()

    if return_code != 0:
        print("打包失败！返回码:", return_code)
        return

    print("打包成功！")

    # 找到原始 exe 并重命名
    exe_path = os.path.join(output_dir, "main.dist", "main.exe")
    renamed_exe_path = os.path.join(output_dir, "main.dist", target_exe_name)

    if os.path.exists(exe_path):
        os.rename(exe_path, renamed_exe_path)
        print(f"已将 main.exe 重命名为 {target_exe_name}")
    else:
        print("❌ 未找到 main.exe，跳过重命名")

    # 压缩打包目录到 dist 目录下
    dist_dir_to_zip = os.path.join(output_dir, "main.dist")
    zip_path = os.path.join(output_dir, f"{project_name}.zip")

    print(f"开始压缩目录 {dist_dir_to_zip} 为 {zip_path}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dist_dir_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir_to_zip)
                zipf.write(file_path, arcname)

    print("✅ 压缩完成:", zip_path)


if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    run_nuitka(project_dir)
