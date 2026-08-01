
def _assert_no_fusion_types(avals: Sequence[core.AbstractValue]):
  if any(_is_fusion_type(aval) for aval in avals):
    raise NotImplementedError(f"Fusion type found in avals: {avals}")

