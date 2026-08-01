
def apply_updates(params: base.Params, updates: base.Updates) -> base.Params:
  """Applies an update to the corresponding parameters.

  This is a utility functions that applies an update to a set of parameters, and
  then returns the updated parameters to the caller. As an example, the update
  may be a gradient transformed by a sequence of`GradientTransformations`. This
  function is exposed for convenience, but it just adds updates and parameters;
  you may also apply updates to parameters manually, using `jax.tree.map`
  (e.g. if you want to manipulate updates in custom ways before applying them).

  Args:
    params: a tree of parameters.
    updates: a tree of updates, the tree structure and the shape of the leaf
      nodes must match that of `params`.

  Returns:
    Updated parameters, with same structure, shape and type as `params`.
  """
  return jax.tree.map(
      lambda p, u: (
          None if p is None else jnp.asarray(p + u).astype(jnp.asarray(p).dtype)
      ),
      params,
      updates,
      is_leaf=lambda x: x is None,
  )

