import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.init as init
from torch.optim.lr_scheduler import StepLR
import matplotlib.pyplot as plt

# 检查是否有 GPU，如果有则使用 GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
# model = QuadraticModel()
model = QuadraticModel().to(device)

# 使用 Adam 优化器
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 创建损失函数
criterion = nn.MSELoss()

# 示例输入数据 (X)
x_data = torch.linspace(1.0, 100.0, steps=100).view(-1, 1)  # 更多的训练数据
# x_data = torch.linspace(1.0, 50.0, steps=50).view(-1, 1)  # 使用更多的数据点
y_data = 3 + 2 * x_data + 1 * x_data**2
losses = []  # 用来存储每次epoch的损失
epochs = range(1,100001)  # 训练次数
# 打印输入和目标数据，确保没有问题
print("Input data:", x_data)
print("Target data:", y_data)

# 训练模型
# scheduler = StepLR(optimizer, step_size=1, gamma=0.1)  # 每100个epoch降低学习率
# for epoch in range(10000):  # 增加训练次数
for epoch in epochs:  # 增加训练次数
    # 前向传播
    y_pred = model(x_data)

    # 计算损失
    loss = criterion(y_pred, y_data)

    # 更新损失列表
    losses.append(loss.item())

    # 梯度清零
    optimizer.zero_grad()

    # 反向传播
    loss.backward()

    # 更新参数
    optimizer.step()

    # 每 100 次打印一次损失
    # if (epoch + 1) % 100 == 0:
    if epoch % 100 == 0:
        print(f'Epoch [{epoch}/100], Loss: {loss.item():.4f}')
        # print(f'Epoch [{epoch + 1}/100], Loss: {loss.item():.4f}')

    # scheduler.step()  # 调整学习率


# 打印训练后的参数
print(f"Trained parameters: b = {model.b.item()}, w1 = {model.w1.item()}, w2 = {model.w2.item()}")

# 绘制损失图
# plt.figure(figsize=(10,6))
# plt.plot(epochs, losses, label='Training Loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.title('Training Loss over Epochs')
# plt.grid(True)
# plt.legend()
# plt.show()

# 创建子图
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
#
# 绘制X_data, Y_data的散点图
ax[0].scatter(x_data.numpy(), y_data.numpy(), color='blue', label='Data points')
ax[0].set_title('X_data vs Y_data')
ax[0].set_xlabel('X_data')
ax[0].set_ylabel('Y_data')
ax[0].legend()
ax[0].grid(True)
#
# 绘制损失变化的曲线图
# ax[1].plot(losses, color='red', label='Loss')
ax[1].plot(epochs, losses, color='red', marker='o', label='Loss')
ax[1].set_title('Loss vs Epoch')
ax[1].set_xlabel('Epoch')
ax[1].set_ylabel('Loss')
ax[1].legend()
ax[1].grid(True)
#
# 显示图形
plt.tight_layout()
plt.show()


