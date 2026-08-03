from typing import Any

def _addupdate_abstract_eval(ref_aval: AbstractRef,
                             val_aval: core.AbstractValue,
                             *args: Any, tree):
  transforms = tree_util.tree_unflatten(tree, args)
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"`addupdate` must be called on `Ref` types: {ref_aval}.")
  if isinstance(ref_aval.inner_aval, core.ShapedArray):
    expected_out_ty = transform_type(transforms, ref_aval.inner_aval)
    assert isinstance(val_aval, core.ShapedArray)
    assert isinstance(expected_out_ty, core.ShapedArray)
    if expected_out_ty.shape != val_aval.shape:
      raise ValueError(
          "Invalid shape for `addupdate`. "
          f"Ref shape: {ref_aval.shape}. "
          f"Expected shape: {expected_out_ty.shape}. "
          f"Value shape: {val_aval.shape}. "
          f"Transforms: {transforms}. "
      )
    if expected_out_ty.dtype != val_aval.dtype:
      raise ValueError("Invalid dtype for `addupdate`. "
                       f"Ref dtype: {ref_aval.dtype}. "
                       f"Value shape: {val_aval.dtype}. ")
    out_sharding = expected_out_ty.sharding
    if ((out_sharding.mesh._any_axis_explicit or
         val_aval.sharding.mesh._any_axis_explicit) and
        out_sharding != val_aval.sharding):
      raise ValueError("Invalid sharding for `addupdate`. "
                       f"Ref sharding: {ref_aval.sharding}. "
                       f"Value sharding: {val_aval.sharding}. ")
  else:
    # Check that the transforms are valid
    if transforms:
      raise ValueError("Cannot index non-shaped array with nontrivial indices.")
  return [], {AccumEffect(0)}

