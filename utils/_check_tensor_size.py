import math


def _check_tensor_size(shape: tuple[int | pallas_core.Squeezed, ...]):
  size = math.prod(1 if isinstance(d, pallas_core.Squeezed) else d
                   for d in shape)
  power_of_2 = (size & (size - 1)) == 0
  if not power_of_2:
    raise ValueError(
        "The Pallas Triton lowering currently requires that all "
        "operations have array arguments and results whose size "
        "is a power of 2. Encountered an array of "
        f"shape {shape}")

