
def _get_ind(f, ind):
  return lambda *args, **kwargs: f(*args, **kwargs)[ind]

