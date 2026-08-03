from typing import Callable, Union

def _mask_callable(
    mask: Union[base.PyTree, Callable[[base.Params], base.PyTree]],
):
  callable_leaves = jax.tree.leaves(jax.tree.map(callable, mask))
  return (len(callable_leaves) > 0) and all(callable_leaves)  # pylint:disable=g-explicit-length-test

