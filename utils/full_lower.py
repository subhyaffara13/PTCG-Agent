
def full_lower(val):
  if isinstance(val, Tracer):
    return val.full_lower()
  else:
    return val

