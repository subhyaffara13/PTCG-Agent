
def _create_str(x, prefix):
  x_str = f"{','.join(i for i in x)}"
  x_str = x_str if len(x) == 1 else f"({x_str})"
  return f"{prefix}:{x_str}, "

