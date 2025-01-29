import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.init as init
from torch.optim.lr_scheduler import StepLR
import matplotlib.pyplot as plt

# 定义模型
class QuadraticModel(nn.Module):
    def __init__(self):
        super(QuadraticModel, self).__init__()
        self.w1 = nn.Parameter(torch.randn(1))  # 权重 w (用于 X)
        self.w2 = nn.Parameter(torch.randn(1))  # 权重 w (用于 X^2)
        self.b = nn.Parameter(torch.randn(1))  # 偏置 b

        # 进行参数初始化
        init.normal_(self.w1, mean=0, std=0.01)  # 使用较小的标准差
        init.normal_(self.w2, mean=0, std=0.01)  # 使用较小的标准差
        init.normal_(self.b, mean=0, std=0.01)  # 使用较小的标准差

    def forward(self, x):
        return self.b + self.w1 * x + self.w2 * x ** 2  # y = b + w1*X + w2*X^2


# 初始化模型
model = QuadraticModel()

# 使用 Adam 优化器
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 创建损失函数
criterion = nn.MSELoss()

# 示例输入数据 (X)
x_data = torch.linspace(1.0, 100.0, steps=100).view(-1, 1)  # 更多的训练数据
# x_data = torch.linspace(1.0, 50.0, steps=50).view(-1, 1)  # 使用更多的数据点
y_data = 3 + 2 * x_data + 1 * x_data**2

# 打印输入和目标数据，确保没有问题
print("Input data:", x_data)
print("Target data:", y_data)

# 训练模型
# scheduler = StepLR(optimizer, step_size=100, gamma=0.1)  # 每100个epoch降低学习率
for epoch in range(10000):  # 增加训练次数
    # 前向传播
    y_pred = model(x_data)

    # 计算损失
    loss = criterion(y_pred, y_data)

    loses =

    # 梯度清零
    optimizer.zero_grad()

    # 反向传播
    loss.backward()

    # 更新参数
    optimizer.step()

    # 每 100 次打印一次损失
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/1000], Loss: {loss.item():.4f}')

    # scheduler.step()  # 调整学习率


# 打印训练后的参数
print(f"Trained parameters: b = {model.b.item()}, w1 = {model.w1.item()}, w2 = {model.w2.item()}")
