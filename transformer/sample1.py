# Re-importing required libraries and re-plotting the graph after reset
import numpy as np
import matplotlib.pyplot as plt

# Parameters
a = 0.03  # 将 a 从 0.02 改为 0.03
b = 0.05
p = 0.5

# Range for investment proportion f
f = np.linspace(0, 1, 500)

# Function R
R = (1 + f * b) ** p * (1 - f * a) ** (1 - p)
#
# # Plotting
# plt.figure(figsize=(8, 6))
# plt.plot(f, R, label=r"$R = (1 + fb)^p (1 - fa)^{1-p}$")
# plt.title("Investment Function R vs f", fontsize=14)
# plt.xlabel("Investment Proportion (f)", fontsize=12)
# plt.ylabel("R", fontsize=12)
# plt.axhline(1, color='gray', linestyle='--', linewidth=0.8, label="Baseline (R=1)")
# plt.grid(alpha=0.5)
# plt.legend(fontsize=12)
# plt.show()

# Identify regions where R > 1
f_above_1 = f[R > 1]
R_above_1 = R[R > 1]

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(f, R, label=r"$R = (1 + fb)^p (1 - fa)^{1-p}$", color='blue')
plt.fill_between(f_above_1, 1, R_above_1, color='green', alpha=0.3, label="R > 1")
plt.axhline(1, color='gray', linestyle='--', linewidth=0.8, label="Baseline (R=1)")
plt.title("Investment Function R vs f", fontsize=14)
plt.xlabel("Investment Proportion (f)", fontsize=12)
plt.ylabel("R", fontsize=12)
plt.grid(alpha=0.5)
plt.legend(fontsize=12)
plt.show()