from typing import Any, Callable

def _make_prng_wrapped_fun(
    fun: Callable[..., Any],
    prng_in_info: dict[int, str],
    prng_out_info: dict[int, str],
) -> Callable[..., Any]:
  """Wraps a function to handle PRNG key conversion on the worker side.

  On the worker, IFRT passes physical arrays for PRNG key inputs.  This wrapper
  converts them back to PRNG key arrays before calling the user function, and
  converts any PRNG key outputs back to physical arrays before returning them to
  IFRT.

  Args:
    fun: The original user function.
    prng_in_info: Mapping from input leaf index to PRNG impl.
    prng_out_info: Mapping from output leaf index to PRNG impl.

  Returns:
    A wrapped function that handles PRNG conversion transparently.
  """

  @wraps(fun)
  def wrapped_fun(*args, **kwargs):
    # Wrap physical inputs to PRNG keys before calling the user function.
    args_leaves, treedef = tree_util.tree_flatten((args, kwargs))
    args_leaves = _wrap_prng_keys(args_leaves, prng_in_info)
    args, kwargs = tree_util.tree_unflatten(treedef, args_leaves)

    result = fun(*args, **kwargs)

    # Unwrap PRNG key outputs to physical before returning to IFRT.
    result_leaves, out_treedef = tree_util.tree_flatten(result)
    result_leaves = _unwrap_prng_keys(result_leaves, prng_out_info)
    return tree_util.tree_unflatten(out_treedef, result_leaves)

  return wrapped_fun

