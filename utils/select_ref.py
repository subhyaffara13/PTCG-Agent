
def select_ref(idx: jax_typing.Array, *refs) -> state_types.TransformedRef:
  """Selects a ref from a list of refs based on the runtime value of a scalar index.

  This is currently only supported for DMA operations and at the top level of a
  ref. It can wrap other ref operations like `at` underneath.

  Example::

    x_ref = pl.select_ref(idx, x0_ref.at[...], x1_ref)
    pltpu.async_copy(x_ref, y_ref, sem).wait()

  Args:
    idx: A scalar array specifying which ref to select.
    *refs: A sequence of refs to select from.

  Returns:
    A TransformedRef that represents the selection.
  """
  if len(refs) <= 1:
    raise ValueError("At least two refs are required for pl.select_ref.")
  return state_types.TransformedRef(
      ref=refs,
      transforms=(state_types.SelectTransform(idx),),
  )

