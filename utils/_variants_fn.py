
def _variants_fn(test_object, **which_variants) -> VariantsTestCaseGenerator:
  """Implements `variants` and `all_variants`."""

  # Convert keys to enum entries.
  which_variants = {
      ChexVariantType[name.upper()]: var
      for name, var in which_variants.items()
  }
  if isinstance(test_object, VariantsTestCaseGenerator):
    # Merge variants for nested wrappers.
    test_object.add_variants(which_variants)
  else:
    test_object = VariantsTestCaseGenerator(test_object, which_variants)

  return test_object

