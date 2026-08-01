
def _elementwise_inline_asm_abstract_eval(
    *avals: jax_core.ShapedArray, result_shape_dtypes, **kwargs
) -> Sequence[jax_core.ShapedArray]:
  del kwargs  # Unused.
  if not all(x.shape == y.shape for x, y in zip(avals, avals[1:])):
    raise ValueError(
        "All arguments of elementwise_inline_asm must have the same shape"
    )
  return [jax_core.ShapedArray(s.shape, s.dtype) for s in result_shape_dtypes]

