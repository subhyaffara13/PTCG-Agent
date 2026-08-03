from typing import Any

def _swap_abstract_eval(*avals_flat, args_tree, **_):
  ref, transforms, val, mask = args_tree.unflatten(avals_flat)
  assert transforms is not None
  transformed_ref = pallas_core.TransformedRef(ref, transforms)
  expected_output_shape = transformed_ref.shape
  expected_output_dtype = transformed_ref.dtype
  if expected_output_shape != val.shape:
    raise ValueError(
        f"Invalid shape for `swap`. Ref shape: {ref.shape}. "
        f"Value shape: {val.shape}. Transforms: {transforms}. "
    )
  if expected_output_dtype != val.dtype:
    raise ValueError(
        f"Invalid dtype for `swap`. Ref dtype: {expected_output_dtype}. "
        f"Value dtype: {val.dtype}. "
    )
  return (
      jax_core.ShapedArray(expected_output_shape, expected_output_dtype),
      {state.WriteEffect(0)},
  )


def _swap_abstract_eval(ref_aval: AbstractRef,
                        val_aval: core.AbstractValue,
                        *args: Any, tree):
  transforms = tree_util.tree_unflatten(tree, args)
  if transforms and ref_aval.inner_aval.is_high:
    # TODO(mattjj): aval.is_high does not imply the existence of ref_swap_abstract_aval.
    return ref_aval.inner_aval.ref_swap_abstract_eval(  # pyrefly: ignore[missing-attribute]
        ref_aval, val_aval, *args, tree=tree)
  out_aval: core.AbstractValue
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"`swap` must be called on `Ref` types: {ref_aval}.")
  if isinstance(val_aval, AbstractRef):
    raise ValueError("Cannot store a Ref into another Ref. "
                     "Did you forget to load from it using `[...]`?")
  if isinstance(ref_aval.inner_aval, core.ShapedArray):
    assert isinstance(val_aval, core.ShapedArray)
    expected_out_ty = transform_type(transforms, ref_aval.inner_aval)
    assert isinstance(expected_out_ty, core.ShapedArray)
    if expected_out_ty.shape != val_aval.shape:
      raise ValueError("Invalid shape for `swap`. "
                       f"Ref shape: {ref_aval.shape}. "
                       f"Expected shape: {expected_out_ty.shape}. "
                       f"Value shape: {val_aval.shape}. "
                       f"Transforms: {transforms}. ")
    if expected_out_ty.dtype != val_aval.dtype:
      raise ValueError(
          "Invalid dtype for `swap`. "
          f"Ref dtype: {expected_out_ty.dtype}. "
          f"Value dtype: {val_aval.dtype}. "
      )
    out_aval = expected_out_ty
  else:
    if transforms:
      raise ValueError("Cannot index non-shaped array with nontrivial indices.")
    out_aval = ref_aval.inner_aval
  return (out_aval, {WriteEffect(0)})


def _swap_abstract_eval(ref, x, *args, has_mask, tree, add):
  flat_transforms = args[:-1] if has_mask else args
  tref = state_types.TransformedRef(
      ref, jax.tree.unflatten(tree, flat_transforms))
  if has_mask:
    mask = args[-1]
    if mask.dtype != jnp.bool:
      raise TypeError(f"Mask must be a boolean array, got {mask.dtype}")
    if mask.shape != tref.shape:
      raise ValueError(f"Mask must have shape {tref.shape}, got {mask.shape}")
  if ref.dtype != x.dtype:
    raise TypeError(
        f"Ref and value must have the same dtype, got {ref.dtype} and {x.dtype}"
    )
  if tref.shape != x.shape:
    raise ValueError(f"Value must have shape {tref.shape}, got {x.shape}")
  effects: set[jax_core.Effect] = {state_types.WriteEffect(0)}
  if add:
    effects.add(state_types.ReadEffect(0))
  return x, effects

