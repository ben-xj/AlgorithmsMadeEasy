"""
solve the following problem with Lagrange Multiplier method
min f(x) = -3x[0] - 5x[1]
s.t. x[0] + x[2] = 4
    2x[1] + x[3] = 12
    3x[0] + 2x[1] + x[4] = 18
    x[0], x[1], x[2], x[3], x[4] >= 0
"""

import torch


def lagrangian_function(x, lambda_):
    return f(x) + lambda_ @ (A @ x - b)


def f(x):
    return c @ x

 
def update_x(x):
    """ update x with gradient descent """
    new_x = x - eta * x.grad
    x.data = new_x.clamp(min=0)


def update_lambda(lambda_):
    new_lambda = lambda_ - lambda_.grad
    lambda_.data = new_lambda


def pprint(i, x, lambda_):
    print(
        f'\n{i+1}th iter, L:{lagrangian_function(x, lambda_):.2f}, f: {f(x):.2f}')
    print(f'x: {x}')
    print(f'lambda: {lambda_}')
    print("constraints violation: ")
    print(A @ x - b)


def solve(x, lambda_):
    for i in range(100):
        pprint(i, x, lambda_)
        lagrangian_function(x, lambda_).backward()
        update_x(x)
        update_lambda(lambda_)
        x.grad.zero_()
        lambda_.grad.zero_()


if __name__ == '__main__':
    eta = 0.03
    """
    min f(x) = c^T x
    s.t. Ax = b
    x >= 0
    """
    c = torch.tensor([-3, -5, 0, 0, 0], dtype=torch.float32)
    A = torch.tensor([[1, 0, 1, 0, 0], [0, 2, 0, 1, 0], [3, 2, 0, 0, 1]],
                     dtype=torch.float32)
    b = torch.tensor([4, 12, 18], dtype=torch.float32)

    lambda_ = torch.tensor([0, 0, 0], dtype=torch.float32, requires_grad=True)
    x = torch.tensor([2, 0, 2, 0, 0], dtype=torch.float32, requires_grad=True)

    solve(x, lambda_)
