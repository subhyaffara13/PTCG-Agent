from typing import Any

def safe_to_cast(input_dtype_or_value: Any,
                 output_dtype_or_value: Any) -> bool:
  """Check if a dtype/value is safe to cast to another dtype/value

  Args:
    input_dtype_or_value: a dtype or value (to be passed to result_type)
      representing the source dtype.
    output_dtype_or_value: a dtype or value (to be passed to result_type)
      representing the target dtype.

  Returns:
    boolean representing whether the values are safe to cast according to
    default type promotion semantics.

  Raises:
    TypePromotionError: if the inputs have differing types and no type promotion
    path under the current jax_numpy_dtype_promotion setting.

  Examples:

    >>> safe_to_cast('int16', 'float32')
    True
    >>> safe_to_cast('float32', 'int16')
    False
    >>> safe_to_cast('float32', 'complex64')
    True
    >>> safe_to_cast('complex64', 'float32')
    False
  """
  input_dtype = dtype(input_dtype_or_value)
  output_dtype = dtype(output_dtype_or_value)
  if input_dtype == output_dtype:
    return True
  # We deliberately use output_dtype rather than output_dtype_or_value here:
  # this effectively treats the output dtype as always strongly-typed.
  return result_type(input_dtype_or_value, output_dtype) == output_dtype

