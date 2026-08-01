
def IteratedMatchingPennies(iterations: int, batch_size=1):
  return IteratedMatrixGame(
      payoff_matrix=np.array([[[1, -1], [-1, 1]], [[-1, 1], [1, -1]]]),
      iterations=iterations,
      batch_size=batch_size,
      include_remaining_iterations=False,
  )

