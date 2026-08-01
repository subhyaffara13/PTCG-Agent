
def replicate_trailing_dims(ctx, val: ir.Value, aval) -> ir.Value:
  # Set the sharding of extended dtypes to be UNCONSTRAINED
  # (i.e. XLA will choose) on aval.shape.
  # For the trailing dims i.e. the dimension of key_shape on the base_array,
  # the sharding is set to be REPLICATED always.
  # For example: if the key.shape is (8, 2) and key_data(key).shape is (8, 2, 2),
  # then the sharding will be P(P.UNCONSTRAINED, P.UNCONSTRAINED, None).
  # The below custom call achieves the sharding like above example.
  assert isinstance(aval, core.ShapedArray)
  if config.use_shardy_partitioner.value:
    physical_ndim = core.physical_aval(aval).ndim
    s = SdyArray(
        mesh_shape=None,
        dim_shardings=tuple(
            sharding_impls.SdyDim(axes=(), is_open=i < aval.ndim)
            for i in range(physical_ndim)
        ))
    return wrap_with_sharding_op(ctx, val, aval, s)
  else:
    return wrap_with_sharding_op(
      ctx, val, aval, xc.HloSharding.replicate().to_proto(),
      unspecified_dims=set(range(aval.ndim)))

