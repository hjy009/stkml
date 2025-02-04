
class Encoding:
    def __init__(self, domain_start: float, domain_end: float):
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
        对乱序的数字序列进行编码，计算每个数字的子域范围并保存到实例变量中。
        :param numbers: 输入的数字序列。
        """
        # 对数字排序并去重
        sorted_numbers = sorted(set(numbers))

        if not all(self.domain_start <= num <= self.domain_end for num in sorted_numbers):
            raise ValueError("Some numbers are out of the defined domain range.")

        ranges = {}
        for i, num in enumerate(sorted_numbers):
            if i == 0:
                # 第一个数字：从定义域起点到第一个数字的中间范围
                lower_bound = self.domain_start
                upper_bound = (sorted_numbers[i + 1] - num) / 2 + num
            elif i == len(sorted_numbers) - 1:
                # 最后一个数字：从最后一个数字到定义域终点
                lower_bound = (num - sorted_numbers[i - 1]) / 2 + sorted_numbers[i - 1]
                upper_bound = self.domain_end
            else:
                # 中间数字：从前后两个数字的中间点
                lower_bound = (num - sorted_numbers[i - 1]) / 2 + sorted_numbers[i - 1]
                upper_bound = (sorted_numbers[i + 1] - num) / 2 + num

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

    def decode_ranges(self, indices):
        """
        将解码返回的索引序列转换为对应的范围序列。
        :param indices: 输入的索引序列。
        :return: 对应的范围序列。
        """
        if not self.encoded_ranges:
            raise ValueError("No encoded ranges found. Please run encode() first.")

        # 获取范围序列
        ranges = [self.encoded_ranges[idx] for idx in indices if idx in self.encoded_ranges]
        return ranges

if __name__ == '__main__':
    # 定义域为 [-10, 10]
    encoder = Encoding(domain_start=-10, domain_end=10)

    # 输入乱序且包含重复数字的序列
    numbers = [0, -8, 4, -4, 8, -8, 0]
    # numbers = [ 311,  262,  465,  353,  333,  365,  388,  276,  358,  352,  274,
    #     249,  311,  321,  341,  361, 1182]
    # 对数字序列进行编码
    encoder.encode(numbers)

    # 输出保存的编码范围
    print("Encoded Ranges (by index in sorted order):")
    for idx, range_ in encoder.encoded_ranges.items():
        print(f"Index {idx}: Range {range_}")

    # 解码单个值
    decoded_single = encoder.decode(-9)
    print("\nDecoded Indices for Value -9:")
    print(decoded_single)

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
    # 将解码索引序列转换为范围序列
    decoded_ranges_single = encoder.decode_ranges(decoded_single)
    print("\nDecoded Ranges for Indices [0]:")
    print(decoded_ranges_single)

    # 解码数列并转换为范围序列
    decoded_list = encoder.decode([-9, 5])
    decoded_ranges_list = encoder.decode_ranges(decoded_list)
    print("\nDecoded Ranges for Values [-9, 5]:")
    print(decoded_ranges_list)

