
def unwrap_transformed_memref(
    ref: ir.Value[ir.MemRefType], expected_transforms: ir.ArrayAttr
) -> ir.Value:
  """Uwraps a memref from an unrealized cast and verifies its transforms."""
  transformed_type = transform_type(ref.type, expected_transforms)
  conversion_cast, [result] = _undo_conversion_cast(ref, [transformed_type])

  # Check that the actual transforms match the expected ones.
  if expected_transforms != conversion_cast.attributes["transforms"]:
    raise ValueError(
        f"Expected transforms {expected_transforms} do not match actual"
        f" transforms {conversion_cast.attributes['transforms']}"
    )

  return result

