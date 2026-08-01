
def _maybe_upcast(result_dtype, preferred_element_type, check_bit_width):
  # replicates the logic in shape_inference.cc's MaybeUpcast
  if (preferred_element_type is None or
      result_dtype == preferred_element_type):
    return result_dtype
  if (check_bit_width and not dtypes.issubdtype(result_dtype, np.floating) and
      _bit_width(preferred_element_type) < _bit_width(result_dtype)):
    raise TypeError("`preferred_element_type` must not be narrower than the "
                    "original type, got preferred_element_type of "
                    f"{preferred_element_type} for result type of "
                    f"{result_dtype}.")
  return preferred_element_type

