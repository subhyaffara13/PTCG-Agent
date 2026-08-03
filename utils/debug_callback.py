from typing import Any, Callable

def debug_callback(
    callback: Callable[..., None],
    *args: Any,
    ordered: bool = False,
    partitioned: bool = False,
    **kwargs: Any,
) -> None:
  ...


def debug_callback(
    *,
    ordered: bool = False,
    partitioned: bool = False,
) -> Callable[..., None]:
  ...


def debug_callback(
    callback: Callable[..., None] | None = None,
    *args: Any,
    ordered: bool = False,
    partitioned: bool = False,
    **kwargs: Any,
) -> Callable[..., None] | None:
  """Calls a stageable Python callback.

  For more explanation, see `External Callbacks`_.

  ``jax.debug.callback`` enables you to pass in a Python function that can be
  called inside of a staged JAX program. A ``jax.debug.callback`` follows
  existing JAX transformation *pure* operational semantics, which are therefore
  unaware of side-effects. This means the effect could be dropped, duplicated,
  or potentially reordered in the presence of higher-order primitives and
  transformations.

  We want this behavior because we'd like ``jax.debug.callback`` to be
  "innocuous", i.e. we want these primitives to change the JAX computation as
  little as possible while revealing as much about them as possible, such as
  which parts of the computation are duplicated or dropped.

  ``jax.debug.callback`` supports two ways of being called:

  1. Two-call form (Recommended):
     ``jax.debug.callback(ordered=True)(callback, *args, **kwargs)``
     Options are passed in the first call. The callback and its arguments are
     passed in the second call. No option arguments are accepted in the second
     call.

  2. Single-call form:
     ``jax.debug.callback(callback, *args, ordered=True, **kwargs)``
     (Soft deprecated) Mixing `ordered` and `partitioned` options with callback
     ``kwargs`` is soft deprecated.

  Args:
    callback: A Python callable returning None.
    *args: The positional arguments to the callback.
    ordered: A keyword only argument used to indicate whether or not the staged
      out computation will enforce ordering of this callback w.r.t. other
      ordered callbacks.
    partitioned: If True, then print local shards only; this option avoids an
      all-gather of the operands. If False, print with logical operands; this
      option requires an all-gather of operands first.
    **kwargs: The keyword arguments to the callback.

  Returns:
    None

  See Also:
    - :func:`jax.experimental.io_callback`: callback designed for impure
      functions.
    - :func:`jax.pure_callback`: callback designed for pure functions.
    - :func:`jax.debug.print`: callback designed for printing.

  .. _External Callbacks:
     https://docs.jax.dev/en/latest/notebooks/external_callbacks.html
  """
  def _debug_callback(
      callback: Callable[..., None], *c_args: Any, **c_kwargs: Any
  ):
    if not callable(callback):
      raise TypeError(
          "first argument to jax.debug.callback must be callable, "
          f"but got an object of type {type(callback)}"
      )
    in_tree, dyn_args, static_args = _split_callback_args(c_args, c_kwargs)

    def _flat_callback(*dyn_args_flat):
      all_args = [None] * (len(static_args) + len(dyn_args_flat))
      di = iter(dyn_args_flat)
      for i in range(len(all_args)):
        if i in static_args:
          all_args[i] = static_args[i]
        else:
          all_args[i] = next(di)
      assert next(di, None) is None
      args_, kwargs_ = tree_util.tree_unflatten(in_tree, all_args)
      callback(*args_, **kwargs_)
      return ()

    effect = ordered_debug_effect if ordered else debug_effect
    debug_callback_p.bind(
        *dyn_args,
        callback=_flat_callback,
        effect=effect,
        partitioned=partitioned,
    )

  if callback is not None:
    _debug_callback(callback, *args, **kwargs)
    return None

  if args or kwargs:
    raise TypeError(
        "debug_callback received unexpected arguments in the two-call form:"
        f" {args=} {kwargs=}"
    )
  return _debug_callback

