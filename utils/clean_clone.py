
def clean_clone(x):
  """Remove scopes and tracers from children."""
  if isinstance(x, Module):
    object.__setattr__(
      x, 'children', {k: clean_clone(v) for k, v in x.children.items()}
    )
    object.__setattr__(x, 'scope', None)
  return x

