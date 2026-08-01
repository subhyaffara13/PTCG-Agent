
def _unsupported_lowering_error(platform: str) -> Exception:
  return ValueError(
      f"Cannot lower pallas_call on platform: {platform}. To use Pallas on GPU,"
      " install jaxlib GPU. To use Pallas on TPU, install jaxlib TPU and"
      " libtpu. See https://docs.jax.dev/en/latest/installation.html."
  )

