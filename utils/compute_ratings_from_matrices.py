
def compute_ratings_from_matrices(
    win_matrix: np.ndarray,
    draw_matrix: Optional[np.ndarray] = None,
    smoothing_factor: float = pyspiel.elo.DEFAULT_SMOOTHING_FACTOR,
    max_iterations: int = pyspiel.elo.DEFAULT_MAX_ITERATIONS,
    convergence_delta: float = pyspiel.elo.DEFAULT_CONVERGENCE_DELTA,
) -> np.ndarray:
  """Compute Elo ratings from a win matrix and a draw matrix."""
  options = pyspiel.elo.default_elo_options()
  options.smoothing_factor = smoothing_factor
  options.max_iterations = max_iterations
  options.convergence_delta = convergence_delta
  return np.array(pyspiel.elo.compute_ratings_from_matrices(
      win_matrix=win_matrix.tolist(),
      draw_matrix=(draw_matrix.tolist() if draw_matrix is not None else []),
      options=options,
  ))

