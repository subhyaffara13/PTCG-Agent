
def shape_tensor(ctx: ModuleContext, sizes: Sequence[int | ir.Value]) -> ir.Value:
  int1d = aval_to_ir_type(ctx, core.ShapedArray((1,), np.int32))
  i32_type = aval_to_ir_type(ctx, core.ShapedArray((), np.int32))
  def lower_dim(d):
    if type(d) is int:
      return ir_constant(np.array([d], np.int32))
    else:
      if d.type != i32_type:
        d = hlo.convert(i32_type, d)
      return hlo.reshape(int1d, d)
  ds = map(lower_dim, sizes)
  if not ds:
    return ir_constant(np.array([], np.int32))
  elif len(ds) == 1:
    return ds[0]
  else:
    return hlo.concatenate(ds, i64_attr(0))

