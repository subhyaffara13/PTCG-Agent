import functools
from typing import Any, Callable

def rand_bcsr(rng: np.random.RandomState,
              rand_method: Callable[..., Any]=jtu.rand_default,
              nse: int | float=0.5, n_batch: int=0, n_dense: int=0):
  """Generates a random BCSR array."""
  return functools.partial(_rand_sparse, rng=rng, rand_method=rand_method,
                           nse=nse, n_batch=n_batch, n_dense=n_dense,
                           sparse_format='bcsr')

