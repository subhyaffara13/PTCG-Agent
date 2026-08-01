
def compute_ratings_from_preference_profile(
    profile: base.PreferenceProfile,
    smoothing_factor: float = pyspiel.elo.DEFAULT_SMOOTHING_FACTOR,
    max_iterations: int = pyspiel.elo.DEFAULT_MAX_ITERATIONS,
    convergence_delta: float = pyspiel.elo.DEFAULT_CONVERGENCE_DELTA,
) -> dict[base.AlternativeId, float]:
  """Compute Elo ratings from a win matrix and a draw matrix."""
  options = pyspiel.elo.default_elo_options()
  options.smoothing_factor = smoothing_factor
  options.max_iterations = max_iterations
  options.convergence_delta = convergence_delta
  num_agents = profile.num_alternatives()
  alt_idx = profile.alternatives_dict
  win_matrix = np.zeros((num_agents, num_agents), dtype=int)
  for vote in profile.votes:
    for i in range(len(vote.vote)):
      for j in range(i + 1, len(vote.vote)):
        for _ in range(vote.weight):
          agent_i_idx = alt_idx[vote.vote[i]]
          agent_j_idx = alt_idx[vote.vote[j]]
          win_matrix[agent_i_idx, agent_j_idx] += 1
  ratings_array = elo.compute_ratings_from_matrices(
      win_matrix, smoothing_factor=smoothing_factor,
      max_iterations=max_iterations,
      convergence_delta=convergence_delta,
  )
  alternatives = profile.alternatives
  return {alternatives[i]: ratings_array[i] for i in range(num_agents)}

