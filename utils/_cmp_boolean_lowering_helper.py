
def _cmp_boolean_lowering_helper(primitive, x: Array, y: Array):
  """A helper function for lowering comparison operations for boolean inputs.

  Args:
    primitive: A JAX primitive representing a comparison operation, which is
      one of the following: `lax.eq_p` (equals), `lax.ne_p` (not equals),
      `lax.lt_p` (less than), `lax.le_p` (less than or equal to),
      `lax.gt_p` (greater than), or `lax.ge_p` (greater than or equal to).
    x: A boolean array representing the first operand in the comparison.
    y: A boolean array representing the second operand in the comparison.

  Returns:
    A boolean array that is the result of applying the comparison operation
    between `x` and `y` based on the given primitive.

  Raises:
    ValueError: If an unsupported comparison primitive is provided.
  """
  if primitive == lax.eq_p:
    return jnp.logical_not(jnp.logical_xor(x, y))
  elif primitive == lax.ne_p:
    return jnp.logical_xor(x, y)
  elif primitive == lax.lt_p:
    return jnp.logical_and(jnp.logical_not(x), y)
  elif primitive == lax.le_p:
    return jnp.logical_or(jnp.logical_not(x), y)
  elif primitive == lax.gt_p:
    return jnp.logical_and(x, jnp.logical_not(y))
  elif primitive == lax.ge_p:
    return jnp.logical_or(x, jnp.logical_not(y))
  else:
    raise ValueError(f"Unsupported comparison primitive: {primitive}")

