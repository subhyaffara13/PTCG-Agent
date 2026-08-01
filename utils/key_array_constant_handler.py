
def key_array_constant_handler(val, aval):
  arr = val._base_array
  return mlir.get_constant_handler(type(arr))(arr, aval)

