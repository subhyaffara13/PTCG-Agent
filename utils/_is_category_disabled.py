
def _is_category_disabled(
    category: Category | None,
) -> bool:
  """Check if the error checking behavior for the given category is disabled."""
  if category is None:
    return False
  if category == "nan":
    raise ValueError("nan is deprecated. Use `_set_error_if_nan` instead.")
  if category == "divide":
    raise ValueError(
        "divide is deprecated. Use `_set_error_if_divide_by_zero` instead."
    )
  if category == "oob":
    return config.error_checking_behavior_oob.value == "ignore"
  raise ValueError(f"Invalid category: {category}")

