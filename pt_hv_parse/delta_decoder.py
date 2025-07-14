from typing import Any, Dict, List, Tuple


class DeltaDecoder:
    @staticmethod
    def decode_varint(data: bytes, pos: int) -> Tuple[int, int]:  # ✅ 正确
        """解码变长整数"""
        result = 0
        shift = 0
        while True:
            byte = data[pos]
            pos += 1
            result |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return result, pos

    @staticmethod
    def zigzag_decode(encoded: int) -> int:
        """ZigZag 解码"""
        return (encoded >> 1) ^ -(encoded & 1)

    @staticmethod
    def delta_varint_decode(hex_str: str) -> List[int]:
        """解码单个十六进制字符串为整数序列"""
        byte_data = bytes.fromhex(hex_str)
        if len(byte_data) < 4:
            raise ValueError("Invalid data: insufficient length for base value")

        base_value = byte_data[0] | (byte_data[1] << 8) | (byte_data[2] << 16) | (byte_data[3] << 24)

        decoded = [base_value]
        pos = 4
        last_value = base_value

        while pos < len(byte_data):
            zigzag, pos = DeltaDecoder.decode_varint(byte_data, pos)
            delta = DeltaDecoder.zigzag_decode(zigzag)
            current_value = last_value + delta
            decoded.append(current_value)
            last_value = current_value

        return decoded

    def decode_all(self, data_dict: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        解码整个数据字典，并返回：
        - "individual": 每个十六进制字符串对应的点列表
        - "combined": 所有点拼接后的总序列，x 轴从 0 开始递增
        """
        individual_result = {}
        combined_result = []
        x_index = 0

        hex_list = data_dict.get("pids", [])

        for hex_str in hex_list:
            try:
                values = self.delta_varint_decode(hex_str)
                points = [{"x": i, "y": v} for i, v in enumerate(values)]
                individual_result[hex_str] = points

                for v in values:
                    combined_result.append({"x": x_index, "y": v})
                    x_index += 1
            except Exception as e:
                individual_result[hex_str] = [{"error": str(e)}]

        return {"individual": individual_result, "combined": combined_result}


# 示例调用
if __name__ == "__main__":
    # 示例输入
    example_data = {
        "pids": [
            "E80300000A01",  # [1000, 1005, 1000]
            "640000008601",  # [100, 200]
        ]
    }

    decoder = DeltaDecoder()
    result = decoder.decode_all(example_data)

    from pprint import pprint

    pprint(result)
