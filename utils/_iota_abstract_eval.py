
def _iota_abstract_eval(dtype, shape, dimension, sharding):
  # TODO(mattjj) Generalize shape_like checking to permit dynamic shapes
  _check_shapelike("iota", "shape", shape)
  if not any(dtypes.issubdtype(dtype, t) for t in _num):
    msg = 'iota does not accept dtype {}. Accepted dtypes are subtypes of {}.'
    typename = dtype_to_string(dtype)
    accepted_typenames = (t.__name__ for t in _num)
    raise TypeError(msg.format(typename, ', '.join(accepted_typenames)))
  if not 0 <= dimension < len(shape):
    raise ValueError("iota dimension must be between 0 and len(shape), got "
                     f"{dimension=} for {shape=}")
  if sharding is None:
    sharding = core.get_cur_mesh_sharding(spec=core.P(*[None] * len(shape)))
  return ShapedArray(shape, dtype, sharding=sharding)

