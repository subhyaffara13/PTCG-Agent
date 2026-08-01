
def count_primitive_compiles():
  dispatch.xla_primitive_callable.cache_clear()

  count = [-1]
  try:
    yield lambda: count[0]
  finally:
    count[0] = dispatch.xla_primitive_callable.cache_info().misses

