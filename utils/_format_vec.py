
def _format_vec(vec):
  """Returns a readable format for a vector."""
  full_fmt = "".join(_format_value(v) for v in vec)
  short_fmt = None
  max_len = 250
  vec2int = lambda vec: int("".join("1" if b else "0" for b in vec), 2)
  if len(vec) > max_len:
    if all(v == 0 for v in vec):
      short_fmt = f"zeros({len(vec)})"
    elif all(v in (0, 1) for v in vec):
      sz = (len(vec) + 15) // 16
      # To reconstruct the original vector:
      # binvec = lambda n, x: [int(x) for x in f"{x:0>{n}b}"]
      short_fmt = f"binvec({len(vec)}, 0x{vec2int(vec):0>{sz}x})"
  if short_fmt and len(short_fmt) < len(full_fmt):
    return short_fmt
  else:
    return full_fmt

