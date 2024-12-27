
class Encoding:
    def __init__(self, domain_start: int, domain_end: int):
        """
        初始化动态范围编码器。
        :param domain_start: 数字定义域的起始值。
        :param domain_end: 数字定义域的结束值。
        """
        self.domain_start = domain_start
        self.domain_end = domain_end

    def encode(self, numbers: list):
        """
        对数字序列进行编码，计算每个数字的子域范围。
        :param numbers: 输入的数字序列（必须已排序）。
        :return: 包含每个数字及其对应范围的字典。
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

            ranges[num] = (lower_bound, upper_bound)

        return ranges

    def decode(self, number_range: tuple, ranges: dict):
        """
        解码范围，查找包含范围的数字。
        :param number_range: 输入的范围 (lower, upper)。
        :param ranges: 编码范围字典。
        :return: 包含输入范围的数字列表。
        """
        decoded_numbers = [
            num for num, (lower, upper) in ranges.items()
            if lower <= number_range[0] and upper >= number_range[1]
        ]
        return decoded_numbers


# 定义域为 [0, 100]
encoder = Encoding(domain_start=0, domain_end=100)

# 输入数字序列
numbers = [5, 15, 25, 35, 95]

# 对数字序列进行编码
encoded_ranges = encoder.encode(numbers)
print("Encoded Ranges:")
for num, range_ in encoded_ranges.items():
    print(f"Number {num}: Range {range_}")

# 解码特定范围
decoded_numbers = encoder.decode((0, 10), encoded_ranges)
print("\nDecoded Numbers for Range (0, 10):")
print(decoded_numbers)