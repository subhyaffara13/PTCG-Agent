
def get_cast_tspec_deserialize(
    tspec: dict[str, Any], args: types.RestoreArgs
) -> dict[str, Any]:
  """Creates a Tensorstore spec for casting a param during deserialize."""

  # Cast is not needed dtype is None or JAX random key type
  if args.dtype is not None and not jax.dtypes.issubdtype(
      args.dtype, jax.dtypes.prng_key
  ):
    tspec = {
        'base': tspec,
        'driver': 'cast',
        'dtype': jnp.dtype(args.dtype).name,
    }
  return tspec

