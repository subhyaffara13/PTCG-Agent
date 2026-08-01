
def supports_bfloat16_matmul() -> bool:
  """Does the currently attached CPU support bfloat16 inputs?"""
  return not is_tpu() or tpu_generation() >= 4

