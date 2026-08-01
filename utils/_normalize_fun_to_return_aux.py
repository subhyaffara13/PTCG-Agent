
def _normalize_fun_to_return_aux(fun, has_aux):
  if has_aux:
    return fun
  else:
    return lambda *args, **kwargs: (fun(*args, **kwargs), None)

