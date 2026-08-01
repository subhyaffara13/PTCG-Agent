
def softmax_on_range(number_policies):
  x = np.array(list(range(number_policies)))
  x = np.exp(x-x.max())
  x /= np.sum(x)
  return x

