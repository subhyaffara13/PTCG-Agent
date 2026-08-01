
def prngkeyarray_unflatten(impl, children):
  base_array, = children
  return PRNGKeyArray(impl, base_array)

