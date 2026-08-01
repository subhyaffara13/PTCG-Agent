
def wrap_transformed_memref(
    transformed_memref: ir.Value,
    logical_type: ir.Type,
    transforms: ir.ArrayAttr,
) -> ir.Value:
  """Wraps a transformed memref to an unrealized cast with transforms.

  The return type of the cast is the untransformed logical type.
  """
  conversion_cast = builtin.UnrealizedConversionCastOp(
      [logical_type], [transformed_memref]
  )
  conversion_cast.attributes["transforms"] = transforms
  return conversion_cast.result

