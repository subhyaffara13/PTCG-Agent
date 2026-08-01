
def _lower_single_transformed_ref(f, ref, ref_ty, ref_block_shape, prev_args,
                                  rest_args):
  """Let the lowering callback f run the single-ref transforms for `ref`."""
  assert isinstance(ref, state.TransformedRef) and not ref.multiref
  aval = ref_ty.ref
  if isinstance(aval, state.TransformedRef):
    aval = aval.type

  def new_f(*newf_args):
    prev, (x,), rest = split_list(newf_args, [len(prev_args), 1])
    new_x, _ = _transform_ref(x, aval, ref_ty.ref.shape, ref.transforms)
    return f(*prev, new_x, *rest)

  next_args = (ref.ref, ref_ty.ref, ref_block_shape.ref)
  return _lower_transformed_refs(new_f, prev_args, [next_args] + rest_args)

