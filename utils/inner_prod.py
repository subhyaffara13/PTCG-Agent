
def inner_prod(xs, ys):
  def contract(x, y):
    return np.real(np.dot(np.conj(x).reshape(-1), y.reshape(-1)))
  return tree_reduce(np.add, tree_map(contract, xs, ys))

