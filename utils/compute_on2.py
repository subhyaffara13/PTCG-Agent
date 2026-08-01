
def compute_on2(f=None, *, compute_type, out_memory_spaces,
                compiler_options=None):
  kwargs = dict(compute_type=compute_type, out_memory_spaces=out_memory_spaces,
                compiler_options=compiler_options)
  if f is None:
    return lambda g: _compute_on2(g, **kwargs)
  return _compute_on2(f, **kwargs)

