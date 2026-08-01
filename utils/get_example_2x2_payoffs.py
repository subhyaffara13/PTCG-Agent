
def get_example_2x2_payoffs():
  mean_payoffs = np.random.uniform(-1, 1, size=(2, 2, 2))
  mean_payoffs[0, :, :] = np.asarray([[0.5, 0.85], [0.15, 0.5]])
  mean_payoffs[1, :, :] = 1 - mean_payoffs[0, :, :]
  return mean_payoffs

