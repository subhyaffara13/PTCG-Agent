
def get_payoffs_bernoulli_game(size=(2, 2, 2)):
  """Gets randomly-generated zero-sum symmetric two-player game."""
  too_close = True
  while too_close:
    M = np.random.uniform(-1, 1, size=size)  # pylint: disable=invalid-name
    M[0, :, :] = 0.5 * (M[0, :, :] - M[0, :, :].T)
    M[1, :, :] = -M[0, :, :]
    if np.abs(M[0, 0, 1]) < 0.1:
      too_close = True
    else:
      too_close = False
  return M

