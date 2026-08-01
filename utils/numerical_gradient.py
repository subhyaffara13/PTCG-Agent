
def numerical_gradient(fun, x, eps=np.sqrt(np.finfo(float).eps)):
  fun_0 = fun(x)
  num_grad = [np.zeros_like(xi) for xi in x]
  x_plus_dx = [np.copy(xi) for xi in x]
  for i, xi in enumerate(x):
    for j, xij in enumerate(xi):
      x_plus_dx[i][j] = xij + eps
      num_grad[i][j] = (fun(x_plus_dx) - fun_0) / eps
      x_plus_dx[i][j] = xij
  return num_grad


def numerical_gradient(fun, x, eps=np.sqrt(np.finfo(float).eps)):
  fun_0 = fun(x)
  num_grad = np.zeros_like(x)
  x_plus_dx = np.copy(x)
  for i, xi in enumerate(x):
    x_plus_dx[i] = xi + eps
    num_grad[i] = (fun(x_plus_dx) - fun_0) / eps
    x_plus_dx[i] = xi
  return num_grad

