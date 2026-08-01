
def check_arg(arg: Any):
  if not core.valid_jaxtype(arg):
    raise TypeError(f"Argument '{arg}' of type {type(arg)} is not a valid "
                    "JAX type.")

