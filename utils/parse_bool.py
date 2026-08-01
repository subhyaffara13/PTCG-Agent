
def parse_bool(expr: Expression) -> bool | None:
    if isinstance(expr, NameExpr):
        if expr.fullname == "builtins.True":
            return True
        if expr.fullname == "builtins.False":
            return False
    return None


def ParseBool(text):
  """Parse a boolean value.

  Args:
    text: Text to parse.

  Returns:
    Boolean values parsed

  Raises:
    ValueError: If text is not a valid boolean.
  """
  if text in ('true', 't', '1', 'True'):
    return True
  elif text in ('false', 'f', '0', 'False'):
    return False
  else:
    raise ValueError('Expected "true" or "false".')

