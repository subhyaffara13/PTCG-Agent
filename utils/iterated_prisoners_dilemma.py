
def IteratedPrisonersDilemma(iterations: int, batch_size=1):
  return IteratedMatrixGame(
      payoff_matrix=np.array([[[-1, -1], [-3, 0]], [[0, -3], [-2, -2]]]),
      iterations=iterations,
      batch_size=batch_size,
      include_remaining_iterations=False,
  )

