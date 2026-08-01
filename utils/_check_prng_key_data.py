
def _check_prng_key_data(impl, key_data: typing.Array):
  ndim = len(impl.key_shape)
  if not all(hasattr(key_data, attr) for attr in ['ndim', 'shape', 'dtype']):
    raise TypeError("JAX encountered invalid PRNG key data: expected key_data "
                    f"to have ndim, shape, and dtype attributes. Got {key_data}")
  if key_data.ndim < 1:
    raise TypeError("JAX encountered invalid PRNG key data: expected "
                    f"key_data.ndim >= 1; got ndim={key_data.ndim}")
  if key_data.shape[-ndim:] != impl.key_shape:
    raise TypeError("JAX encountered invalid PRNG key data: expected key_data.shape to "
                    f"end with {impl.key_shape}; got shape={key_data.shape} for {impl=}")
  if key_data.dtype not in [np.uint32, float0]:
    raise TypeError("JAX encountered invalid PRNG key data: expected key_data.dtype = uint32; "
                    f"got dtype={key_data.dtype}")

