import json
import re
from typing import Dict, List


class DevPidParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pattern = re.compile(r"DEV:PID:([^\s]+)")  # 匹配 PID 后紧跟非空白字符

    def parse(self) -> Dict[str, List[str]]:
        """
        解析文件中所有包含 DEV:PID: 的行，提取 PID 值。
        返回 JSON 格式的数据结构。
        """
        results = []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = self.pattern.search(line)
                    if match:
                        pid = match.group(1)
                        results.append(pid)
        except Exception:
            # 失败时仍返回 pids 字段，只是为空列表
            return {"pids": []}

        return {"pids": results}

    def to_json_string(self) -> str:
        """
        以 JSON 字符串格式返回解析结果。
        """
        return json.dumps(self.parse(), indent=2)


# 示例用法：
if __name__ == "__main__":
    parser = DevPidParser("example.log")
    print(parser.to_json_string())
