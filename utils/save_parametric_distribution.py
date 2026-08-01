
def save_parametric_distribution(dist: distribution.ParametricDistribution,
                                 filename: str):
  """Saves the parametric distribution to a Pickle file."""
  with gfile.Open(filename, "wb") as f:
    pickle.dump(dist.get_params(), f, protocol=pickle.DEFAULT_PROTOCOL)

