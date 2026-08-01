
def colorized(x, /):
  c = REPR_CONTEXT.current_color
  if isinstance(x, list):
    return f'{c.PAREN}[{c.END}{", ".join(map(lambda i: colorized(i), x))}{c.PAREN}]{c.END}'
  elif isinstance(x, tuple):
    if len(x) == 1:
      return f'{c.PAREN}({c.END}{colorized(x[0])},{c.PAREN}){c.END}'
    return f'{c.PAREN}({c.END}{", ".join(map(lambda i: colorized(i), x))}{c.PAREN}){c.END}'
  elif isinstance(x, dict):
    open, close = '{', '}'
    return f'{c.PAREN}{open}{c.END}{", ".join(f"{c.STRING}{k!r}{c.END}: {colorized(v)}" for k, v in x.items())}{c.PAREN}{close}{c.END}'
  elif isinstance(x, set):
    open, close = '{', '}'
    return f'{c.PAREN}{open}{c.END}{", ".join(map(lambda i: colorized(i), x))}{c.PAREN}{close}{c.END}'
  elif isinstance(x, type):
    return f'{c.TYPE}{x.__name__}{c.END}'
  elif isinstance(x, bool):
    return f'{c.BOOL}{x}{c.END}'
  elif isinstance(x, int):
    return f'{c.INT}{x}{c.END}'
  elif isinstance(x, str):
    return f'{c.STRING}{x!r}{c.END}'
  elif isinstance(x, float):
    return f'{c.FLOAT}{x}{c.END}'
  elif x is None:
    return f'{c.NONE}{x}{c.END}'
  elif isinstance(x, Representable):
    return get_repr(x)
  else:
    return repr(x)

