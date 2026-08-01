
def has_user_context(e):
  while e is not None:
    if isinstance(e, JaxStackTraceBeforeTransformation):
      return True
    e = e.__cause__
  return False

