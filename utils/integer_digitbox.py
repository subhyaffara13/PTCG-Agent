
def integer_digitbox(
    value: int, *, label: str | None = None, size: str = "1em"
) -> figures_impl.TreescopeFigure:
  """Returns a "digitbox" rendering of a single integer.

  Args:
    value: Integer value to render.
    label: Optional label to draw next to the digitbox.
    size: Size for the rendering as a CSS length. "1em" means render it at the
      current font size.

  Returns:
    A renderable object showing the digitbox rendering for this integer.
  """
  value = int(value)

  render_args = json.dumps({"value": value})
  size_attr = html_escaping.escape_html_attribute(size)
  # Note: We need to save the parent of the treescope-run-here element first,
  # because it will be removed before the runSoon callback executes.
  src = (
      f'<span class="inline_digitbox" style="font-size: {size_attr}">'
      '<treescope-run-here><script type="application/octet-stream">'
      "const parent = this.parentNode;"
      "const defns = this.getRootNode().host.defns;"
      "defns.runSoon(() => {"
      f"defns.arrayviz.renderOneDigitbox(parent, {render_args});"
      "});"
      "</script></treescope-run-here>"
      "</span>"
  )
  rendering = arrayviz_impl.ArrayvizDigitboxRendering(src)
  if label:
    return figures_impl.TreescopeFigure(
        basic_parts.siblings(
            rendering,
            common_styles.custom_style(
                basic_parts.text(f" {label}"), "color:gray; font-size: 0.5em"
            ),
        )
    )
  else:
    return figures_impl.TreescopeFigure(rendering)

