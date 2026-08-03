from typing import Any

def process_allgather(in_tree, tiled: bool | None = None):
  """All-gather data from all hosts."""
  if is_pathways_backend():
    return in_tree
  return multihost_utils.process_allgather(in_tree, tiled=tiled)


def process_allgather(in_tree: Any, tiled: bool = False) -> Any:
  """Gather data from across processes.

  Args:
    in_tree: pytree of arrays - each array _must_ have the same shape across the
      hosts.
    tiled: Whether to stack or concat the output. Defaults to False i.e. stack
      into a new positional axis at index 0.

  Returns:
    Pytrees of numpy arrays.
      * If the input is a non-fully addressable jax.Array, then the data is
        fully replicated.
      * If the input is numpy array or fully addressable jax.Array, then the
        output shape is dependent on the `tiled` argument.
        If its False, then the output will be stacked else concatenated.
      * If the input is a scalar, then the output will be stacked.
  """

  def _pjit(inp):
    return _handle_array_process_allgather(inp, tiled)
  return jax.tree.map(_pjit, in_tree)

