import torch

def f(x):
    return x**3

x = torch.tensor(2.0, requires_grad=True)
z = x ** 3 # 3x^2
# z = f(x)
z.backward()
print(x.grad)

x = torch.tensor(1.0, requires_grad=True)
y = x ** 2 # 2x
z = x ** 3 # 3x^2
y.backward()
print(x.grad) 
x.grad.zero_()

z.backward()
print(x.grad) 


x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x**2
y.sum().backward() 
print(x.grad) 

# x = x - x.grad
# y = x**2
# y.sum().backward()

# print(x.grad)

new_x = x - x.grad
x.data = new_x

y = x ** 2
y.sum().backward()

print(x.grad)