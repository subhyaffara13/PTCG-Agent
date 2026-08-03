from typing import Any

def _get_call_flops(
  c: module_lib._CallInfo,
  compute_flops: bool,
  compute_vjp_flops: bool,
) -> tuple[int, int]:
  """Return the FLOPs of executing the call `c` in the call stack.

  Does not perform actual computation / compilation / memory allocation, but
  still introduces overhead for large modules.

  Args:
    c: ``_CallInfo``.
    compute_flops: whether to compute forward pass FLOPs. Return `-1` otherwise.
    compute_vjp_flops: whether to compute backward pass FLOPs. Return `-1`
      otherwise.

  Returns:
    FLOPs of executing forward pass of `c`, and its VJP.
  """

  if not compute_flops and not compute_vjp_flops:
    return -1, -1

  rngs = jax.tree_util.tree_map(
      lambda x: x.rng, c.rngs, is_leaf=lambda x: isinstance(x, LazyRng)
  )

  args = jax.tree_util.tree_map(_from_value_representation, c.args)
  kwargs = jax.tree_util.tree_map(_from_value_representation, c.kwargs)

  leaves, treedef = jax.tree_util.tree_flatten((args, kwargs))
  dynamic_leaves = []
  dynamic_idxs = []
  for i, arg in enumerate(leaves):
    if isinstance(arg, jax.ShapeDtypeStruct):
      dynamic_leaves.append(arg)
      dynamic_idxs.append(i)

  def _get_inputs(dynamic_leaves):
    new_leaves: list[Any] = leaves.copy()
    for i, arg in zip(dynamic_idxs, dynamic_leaves):
      new_leaves[i] = arg
    return treedef.unflatten(new_leaves)

  def init(rngs, dynamic_leaves):
    """`c.module.init` closed over static keyword arguments."""
    args, kwargs = _get_inputs(dynamic_leaves)
    return c.module.init(
      rngs,
      *args,
      method=c.method,
      mutable=c.mutable,
      **kwargs,
    )

  variables = jax.eval_shape(init, rngs, dynamic_leaves)

  def apply(variables, rngs, dynamic_leaves):
    """`c.module.apply` closed over static keyword arguments."""
    args, kwargs = _get_inputs(dynamic_leaves)
    return c.module.apply(
      variables,
      *args,
      rngs=rngs,
      method=c.method,
      mutable=c.mutable,
      **kwargs,
    )

  # Forward pass FLOPs
  if compute_flops:
    flops = _get_flops(apply, variables, rngs, dynamic_leaves)
  else:
    flops = -1

  if compute_vjp_flops:
    # Backward pass FLOPs
    def apply_vjp(variables, rngs, dynamic_leaves):
      """VJP of `c.module.apply` closed over static keyword arguments."""
      out, vjp_fn = jax.vjp(apply, variables, rngs, dynamic_leaves)
      return vjp_fn(out)

    vjp_flops = _get_flops(apply_vjp, variables, rngs, dynamic_leaves)
  else:
    vjp_flops = -1

  return flops, vjp_flops

