
def _maybe_render(x):
  return x.render() if hasattr(x, 'render') else repr(x)

