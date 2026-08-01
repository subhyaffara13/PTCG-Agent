
def _set_error_if_with_category(
    pred: Array,
    /,
    msg: str,
    category: Category | None = None,
) -> None:
  """Set the internal error state if any element of `pred` is `True`.

  This function is similar to :func:`set_error_if`, but it also takes a category
  argument. The category can be "nan", "divide", or "oob". The error checking
  behavior for each category can be configured using
  :func:`set_error_checking_behavior`. If not provided, there will be no
  category.

  This function is intended for use in JAX internal APIs (e.g., `jax.numpy`)
  to perform category-specific runtime checks tied to the operation being
  performed.
  """
  if _is_category_disabled(category):
    return

  error_check_lib.set_error_if(pred, msg)

