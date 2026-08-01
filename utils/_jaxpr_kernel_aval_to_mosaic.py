
def _jaxpr_kernel_aval_to_mosaic(
    aval: jax_core.AbstractValue,
) -> jax_core.AbstractValue:
  match aval:
    case state_types.AbstractLinVal():
      if dtypes.issubdtype(aval.dtype, jax.numpy.bool_):
        raise NotImplementedError  # TODO(mattjj,sharadmv)
      return aval
    case jax_core.ShapedArray():
      if dtypes.issubdtype(aval.dtype, jax.numpy.bool_):
        return aval.update(dtype=lowering.BOOL_MEMREF_TYPE)
      return aval
    case _:
      raise ValueError(f"Unsupported JAX aval type: {type(aval)}")

