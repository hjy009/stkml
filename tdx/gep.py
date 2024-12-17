import itertools

# 定义变量和常数
variables = ['x', 'y']
constants = ['1', '2']
operators = ['+', '*']


# 定义表达式节点
class Expression:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.left is None and self.right is None:
            return str(self.value)
        return f"({self.left} {self.value} {self.right})"

    def __repr__(self):
        return self.__str__()


# 生成简单表达式
def generate_simple_expressions():
    simple_exprs = []
    for v in variables:
        simple_exprs.append(Expression(v))
    for c in constants:
        simple_exprs.append(Expression(c))
    return simple_exprs


# 生成复合表达式
def generate_expressions(depth):
    if depth == 1:
        return generate_simple_expressions()

    previous_expressions = generate_expressions(depth - 1)
    new_expressions = []

    for left, right in itertools.product(previous_expressions, repeat=2):
        for op in operators:
            new_expressions.append(Expression(op, left, right))

    return new_expressions


# 去重：生成表达式的标准形式
def normalize_expression(expr):
    if expr.left and expr.right:
        left_str = normalize_expression(expr.left)
        right_str = normalize_expression(expr.right)
        if expr.value in ['+', '*']:  # 对于加法和乘法，排序子表达式
            left_str, right_str = sorted([left_str, right_str])
        return f"({left_str} {expr.value} {right_str})"
    return str(expr.value)


# 生成所有表达式并去重
def generate_all_expressions(max_depth):
    unique_expressions = set()
    for depth in range(1, max_depth + 1):
        expressions = generate_expressions(depth)
        for expr in expressions:
            normalized = normalize_expression(expr)
            unique_expressions.add(normalized)
    return unique_expressions

# 生成表达式，指定最大深度
max_depth = 3
expressions = generate_all_expressions(max_depth)

# 打印生成的表达式
print(f"生成的表达式数量: {len(expressions)}")
for expr in sorted(expressions):
    print(expr)
