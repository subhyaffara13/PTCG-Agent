
def _get_rich_repr(obj, console_kwargs):
  f = io.StringIO()
  console = rich.console.Console(file=f, **console_kwargs)
  console.print(obj)
  return f.getvalue()


def _get_rich_repr(obj, console_kwargs):
  f = io.StringIO()
  console = rich.console.Console(file=f, **console_kwargs)
  console.print(obj)
  return f.getvalue()

