from typing import Any

def _lower_multiref_transformed_ref(f, ref, ref_ty, ref_block_shape, args,
                                   rest_refs):
  """Lower f with args as a multiref TransformedRef."""
  assert isinstance(ref, state.TransformedRef) and ref.multiref
  assert isinstance(ref.transforms[0], state_types.MultiRefTransform)
  match ref.transforms[0]:
    case state_types.SelectTransform(idx=idx):
      select_options = list(zip(ref.ref, ref_ty.ref, ref_block_shape.ref))
      return _select_to_ifop(f, args, rest_refs, cast(Any, idx), select_options)
    case _:
      raise ValueError(f"Unsupported transform: {ref.transforms[0]}")

