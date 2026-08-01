
def get_primitive_transpose(p):
  try:
    return primitive_transposes[p]
  except KeyError as err:
    raise NotImplementedError(
        "Transpose rule (for reverse-mode differentiation) for '{}' "
        "not implemented".format(p)) from err

