import math


def pprint_bytes(num_bytes: int | float) -> str:
  prefixes = ("", "K", "M", "G", "T")
  if num_bytes <= 0:
    return "0.00B"
  exponent = min(math.floor(math.log(num_bytes, 1000)), len(prefixes) - 1)
  scaled_value = num_bytes / (1000**exponent)
  return f"{scaled_value:.2f}{prefixes[exponent]}B"

