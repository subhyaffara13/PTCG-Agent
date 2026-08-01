
def _display_and_return(
    x: _T,
    *,
    options: str,
    line_code: str | None = None,
) -> _T:
  """Print `x` and return `x`."""
  x_origin = x
  options = {_Options(o) for o in options}

  if _Options.QUIET in options:  # Do not display anything
    return x_origin

  if _Options.SPEC in options:  # Convert to spec
    x = etree.spec_like(x)

  repr_fn = pretty.pretty
  display_fn = IPython.display.display
  if line_code and _Options.SYNTAX_HIGHLIGHT not in options:
    print(line_code + ' = ', end='')
    # When the next element is a `IPython.display`, the next element is
    # displayed on a new line. This is because `display()` create a new
    # <div> section. So use standard `print` when line is displayed.
    display_fn = lambda x: print(pretty.pretty(x))

  if _Options.PPRINT in options:
    repr_fn = epy.pretty_repr
    display_fn = _pretty_display

  if _Options.INSPECT in options:
    inspects.inspect(x)
    return x_origin

  if _Options.ARRAY in options:
    html = array_as_img.array_repr_html(x)
    if html is None:
      print(f'Invalid array to display: {type(x)}')
    else:
      _html_display(html)
    return x_origin

  if _Options.SYNTAX_HIGHLIGHT in options:
    x_repr = repr_fn(x)
    if line_code:
      x_repr = f'{line_code} = {x_repr}'
    _html_display(highlight_util.highlight_html(x_repr))
    return x_origin

  display_fn(x)
  return x_origin

