
def make_random_mask(
    shape: tuple[int, int], sparsity: float, seed: int
) -> np.ndarray:
  """Makes a random attention mask."""
  np.random.seed(seed)
  return np.random.binomial(n=1, p=1.0 - sparsity, size=shape).astype(np.bool_)

