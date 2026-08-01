
def _projection_unit_simplex_jvp(
    primals: list[jax.typing.ArrayLike], tangents: list[jax.typing.ArrayLike]
) -> tuple[jax.Array, jax.Array]:
  (values,) = primals
  (values_dot,) = tangents
  primal_out = _projection_unit_simplex(values)
  supp = primal_out > 0
  card = jnp.count_nonzero(supp)
  tangent_out = supp * values_dot - (jnp.dot(supp, values_dot) / card) * supp
  return primal_out, tangent_out

