"""
solve the following problem with scipy
min f(x) = -3x[0] - 5x[1]
s.t. x[0] + x[2] = 4
    2x[1] + x[3] = 12
    3x[0] + 2x[1] + x[4] = 18
    x[0], x[1], x[2], x[3], x[4] >= 0
"""

from scipy.optimize import linprog
import torch

c = torch.tensor([-3, -5, 0, 0, 0], dtype=torch.float32)
A = torch.tensor([[1, 0, 1, 0, 0], [0, 2, 0, 1, 0], [3, 2, 0, 0, 1]],
                    dtype=torch.float32)
b = torch.tensor([4, 12, 18], dtype=torch.float32)

res = linprog(c, A_eq=A, b_eq=b, bounds=(0, None))
print(res)

# optimal solution:
# fun: -36.0
# x: [ 2.000e+00  6.000e+00  2.000e+00  0.000e+00  0.000e+00]