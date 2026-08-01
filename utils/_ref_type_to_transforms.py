
def _ref_type_to_transforms(ref_type: RefType) -> ir.ArrayAttr:
  """Returns the Mosaic GPU transforms for the given ref type."""
  transform_attrs = [gpu_core.to_transform_attr(t)
                     for t in ref_type.transforms]
  return ir.ArrayAttr.get(transform_attrs)

