
def _vdot(a, b, precision=jax.lax.Precision.HIGHEST):
  """Compute the inner product between two (possibly complex) arrays."""
  if jax.__version__ < '0.7.2':
    return jnp.vdot(a, b, precision=precision)
  assert a.shape == b.shape
  if jax.dtypes.issubdtype(a.dtype, jnp.complexfloating):
    a = jnp.conj(a)
  # jnp.vdot internally uses ravel(), which leads to undesirable comms
  # in distributed setups, and failures when using explicit-sharding.
  mesh = jax.typeof(a).sharding.mesh
  if mesh.are_all_axes_explicit:
    sharding = jax.sharding.NamedSharding(mesh, jax.P())
  else:
    sharding = None
  return jnp.tensordot(a, b, a.ndim, precision=precision, out_sharding=sharding)

