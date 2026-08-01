
def remat3(f=None, /, policy=None, static_argnums=(), static_argnames=()):
  if f is None:
    return partial(partial, _remat3, policy, static_argnums, static_argnames)
  else:
    return partial(_remat3, policy, static_argnums, static_argnames, f)

