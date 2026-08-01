
def all_variants(test_method,
                 with_jit: bool = True,
                 without_jit: bool = True,
                 with_device: bool = True,
                 without_device: bool = True,
                 with_pmap: bool = True) -> VariantsTestCaseGenerator:
  # pylint: enable=redefined-outer-name
  """Equivalent to ``chex.variants`` but with flipped defaults."""
  return _variants_fn(
      test_method,
      with_jit=with_jit,
      without_jit=without_jit,
      with_device=with_device,
      without_device=without_device,
      with_pmap=with_pmap)

