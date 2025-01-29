
class Encoding:
    def __init__(self, domain_start: int, domain_end: int):
        """
        初始化动态范围编码器。
        :param domain_start: 数字定义域的起始值。
        :param domain_end: 数字定义域的结束值。
        """
        self.domain_start = domain_start
        self.domain_end = domain_end
        self.encoded_ranges = {}  # 保存编码后的范围

    def encode(self, numbers: list):
        """
        对数字序列进行编码，计算每个数字的子域范围并保存到实例变量中。
        :param numbers: 输入的数字序列（必须已排序）。
        """
        if not all(self.domain_start <= num <= self.domain_end for num in numbers):
            raise ValueError("Some numbers are out of the defined domain range.")

        ranges = {}
        for i, num in enumerate(numbers):
            if i == 0:
                # 第一个数字：从定义域起点到第一个数字的中间范围
                lower_bound = self.domain_start
                upper_bound = (numbers[i + 1] - num) / 2 + num
            elif i == len(numbers) - 1:
                # 最后一个数字：从最后一个数字到定义域终点
                lower_bound = (num - numbers[i - 1]) / 2 + numbers[i - 1]
                upper_bound = self.domain_end
            else:
                # 中间数字：从前后两个数字的中间点
                lower_bound = (num - numbers[i - 1]) / 2 + numbers[i - 1]
                upper_bound = (numbers[i + 1] - num) / 2 + num

            ranges[i] = (lower_bound, upper_bound)

        self.encoded_ranges = ranges  # 保存编码范围到类实例中

    def decode(self, values):
        """
        解码单个值或数列，返回所属范围的索引列表。
        :param values: 输入单个值或值的数列。
        :return: 每个值所属范围的索引列表。
        """
        if not self.encoded_ranges:
            raise ValueError("No encoded ranges found. Please run encode() first.")

        if isinstance(values, (int, float)):
            # 如果是单个值，转换为列表
            values = [values]

        # 检查每个值所属的范围
        decoded_indices = []
        for value in values:
            for idx, (lower, upper) in self.encoded_ranges.items():
                if lower <= value < upper:
                    decoded_indices.append(idx)
                    break

        return decoded_indices


# 定义域为 [0, 100]
encoder = Encoding(domain_start=0, domain_end=100)

# 输入数字序列
numbers = [5, 15, 25, 35, 95]

# 对数字序列进行编码
encoder.encode(numbers)

# 输出保存的编码范围
print("Encoded Ranges (by index):")
for idx, range_ in encoder.encoded_ranges.items():
    print(f"Index {idx}: Range {range_}")

# 解码单个值
decoded_single = encoder.decode(9)
print("\nDecoded Indices for Value 9:")
print(decoded_single)

# 解码数列
decoded_list = encoder.decode([9, 29,39])
print("\nDecoded Indices for Values [9, 29]:")
print(decoded_list)

print(encoder.encoded_ranges[decoded_list[0]])