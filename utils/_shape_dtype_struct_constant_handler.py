
def _shape_dtype_struct_constant_handler(*args, **kwargs):
  raise TypeError("A ShapeDtypeStruct does not have a value and cannot be "
                  "used as a constant in a JAX function.")

