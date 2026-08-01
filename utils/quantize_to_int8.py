
def quantize_to_int8(
    x: jnp.ndarray,
) -> QuantizedTensor:
  """Quantizes a float array to an int8 QuantizedTensor.

  Args:
    x: Float array to quantize.

  Returns:
    Int8 QuantizedTensor.
  """
  x_scales = get_quantization_scales(x)
  return QuantizedTensor(weight=to_int8(x, x_scales), scales=x_scales)

