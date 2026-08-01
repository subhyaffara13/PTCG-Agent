
def forward_attr(self_, name):
  if name.startswith('def'):
    return getattr(self_.fun, name)
  else:
    raise AttributeError

