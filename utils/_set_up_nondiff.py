
def _set_up_nondiff(f, argnums_, argnames) -> frozenset[int]:
  argnums = set(argnums_)
  if argnames:
    sig = inspect.signature(f)  # needed for static_argnames
    argnums |= set(infer_argnums_and_argnames(sig, None, argnames)[0])
  return frozenset(argnums)

