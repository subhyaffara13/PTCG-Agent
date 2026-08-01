
def concretization_function_error(fun, suggest_astype=False):
  fname = getattr(fun, "__name__", fun)
  fname_context = f"The problem arose with the `{fname}` function. "
  if suggest_astype:
    fname_context += ("If trying to convert the data type of a value, "
                      f"try using `x.astype({fun.__name__})` "
                      f"or `jnp.array(x, {fun.__name__})` instead.")
  if fun is bool:
    def error(self, arg):
      raise TracerBoolConversionError(arg)
  elif fun in (hex, oct, operator.index):
    def error(self, arg):
      raise TracerIntegerConversionError(arg)
  else:
    def error(self, arg):
      raise ConcretizationTypeError(arg, fname_context)
  return error

