import functools
from typing import Callable

def eval_shape(fun: Callable, *args, **kwargs):
  """Compute the shape/dtype of ``fun`` without any FLOPs.

  This utility function is useful for performing shape inference. Its
  input/output behavior is defined by::

    def eval_shape(fun, *args, **kwargs):
      out = fun(*args, **kwargs)
      return jax.tree_util.tree_map(jax.ShapeDtypeStruct.like, out)

  But instead of applying ``fun`` directly, which might be expensive, it uses
  JAX's abstract interpretation machinery to evaluate the shapes without doing
  any FLOPs.

  Using :py:func:`eval_shape` can also catch shape errors, and will raise same
  shape errors as evaluating ``fun(*args, **kwargs)``.

  Args:
    fun: The function whose output shape should be evaluated.
    *args: a positional argument tuple of arrays, scalars, or (nested) standard
      Python containers (tuples, lists, dicts, namedtuples, i.e. pytrees) of
      those types. Since only the ``shape`` and ``dtype`` attributes are
      accessed, one can use :class:`jax.ShapeDtypeStruct` or another container
      that duck-types as ndarrays (note however that duck-typed objects cannot
      be namedtuples because those are treated as standard Python containers).
    **kwargs: a keyword argument dict of arrays, scalars, or (nested) standard
      Python containers (pytrees) of those types. As in ``args``, array values
      need only be duck-typed to have ``shape`` and ``dtype`` attributes.

  Returns:
    out: a nested PyTree containing :class:`jax.ShapeDtypeStruct` objects as leaves.

  For example:

  >>> import jax
  >>> import jax.numpy as jnp
  >>>
  >>> f = lambda A, x: jnp.tanh(jnp.dot(A, x))
  >>> A = jax.ShapeDtypeStruct((2000, 3000), jnp.float32)
  >>> x = jax.ShapeDtypeStruct((3000, 1000), jnp.float32)
  >>> out = jax.eval_shape(f, A, x)  # no FLOPs performed
  >>> print(out.shape)
  (2000, 1000)
  >>> print(out.dtype)
  float32

  All arguments passed via :func:`eval_shape` will be treated as dynamic;
  static arguments can be included via closure, for example using :func:`functools.partial`:

  >>> import jax
  >>> from jax import lax
  >>> from functools import partial
  >>> import jax.numpy as jnp
  >>>
  >>> x = jax.ShapeDtypeStruct((1, 1, 28, 28), jnp.float32)
  >>> kernel = jax.ShapeDtypeStruct((32, 1, 3, 3), jnp.float32)
  >>>
  >>> conv_same = partial(lax.conv_general_dilated, window_strides=(1, 1), padding="SAME")
  >>> out = jax.eval_shape(conv_same, x, kernel)
  >>> print(out.shape)
  (1, 32, 28, 28)
  >>> print(out.dtype)
  float32
  """
  if type(fun) is _jax.PjitFunction:
    return fun.trace(*args, **kwargs).out_info  # pyrefly: ignore[missing-attribute]
  try: hash(fun)
  except TypeError: fun = partial(fun)
  return jit(fun).trace(*args, **kwargs).out_info


def eval_shape(
  f: tp.Callable[..., A],
  *args: tp.Any,
  graph: bool | None = None,
  graph_updates: bool | None = None,
  **kwargs: tp.Any,
) -> A:
  """A \"lifted\" version of `jax.eval_shape <https://jax.readthedocs.io/en/latest/_autosummary/jax.eval_shape.html#jax.eval_shape>`_
    that can handle `flax.nnx.Module <https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/module.html#flax.nnx.Module>`_
    / graph nodes as arguments.

  Similar to ``jax.eval_shape``, it computes the shape/dtype of a function `f` without
    performing any floating point operations (FLOPs) which can be expensive. This can be
    useful for performing shape inference, for example. Unlike `jax.eval_shape`,
    `nnx.eval_shape` will automatically compute the expected sharding based on Flax sharding metadata
    for all Variables not using explicit sharding.

  Args:
    f: the function to evaluate.
    *args: positional arguments to ``f``.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``.
    **kwargs: keyword arguments to ``f``.
"""
  f_call, _, was_bound = _resolve_bound_callable(f)

  if was_bound:
    _raise_bound_method_error('eval_shape')

  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if not graph or not graph_updates:
    if graph:
      args, kwargs = extract.to_tree2((args, kwargs))
    extract.check_no_aliases('eval_shape', args=args, kwargs=kwargs)
    out = jax.eval_shape(
      SimpleEvalShapeFn(f_call, graph=graph), *args, **kwargs
    )
    if graph:
      out = extract.from_tree2(out)
    return out

  args, kwargs = extract.to_tree((args, kwargs))

  @functools.wraps(f)
  def _eval_shape_fn(*args, **kwargs):
    args, kwargs = extract.from_tree((args, kwargs))
    out = f_call(*args, **kwargs)
    return _to_value_metadata(extract.to_tree(out))

  out = jax.eval_shape(_eval_shape_fn, *args, **kwargs)
  return extract.from_tree(_to_variable(out))

