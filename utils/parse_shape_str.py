
def parse_shape_str(s):
  match = _SHAPE_RE.match(s)
  if not match:
    raise ValueError(f'Invalid shape {s}. Valid example: "f32[1,2,3]".'
                     f'Note that dtype must be one of {list(_DT)}')
  dtype = _DT[match.group(1)]
  if match.group(2):
    shape = tuple(int(d.strip()) for d in match.group(2).split(","))
  else:
    shape = ()
  return jax.core.ShapedArray(shape, dtype)

