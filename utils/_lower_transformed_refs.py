
def _lower_transformed_refs(f, args, rest_args):
  """Recursively iterate through TransformedRefs and lower them in the call to f."""
  if rest_args == []:
    return f(*args)
  (ref, ref_ty, ref_block_shape), *rest_refs = rest_args

  if not isinstance(ref, state.TransformedRef):
    return _lower_transformed_refs(f, args + [ref], rest_refs)
  if not ref.multiref:
    return _lower_single_transformed_ref(
        f, ref, ref_ty, ref_block_shape, args, rest_refs
    )
  return _lower_multiref_transformed_ref(
      f, ref, ref_ty, ref_block_shape, args, rest_refs
  )

