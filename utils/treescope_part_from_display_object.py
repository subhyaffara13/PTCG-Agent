from typing import Any

def treescope_part_from_display_object(
    value: Any,
) -> rendering_parts.RenderableTreePart:
  """Converts an arbitrary object to a renderable treescope part if possible.

  Behavior depends on the type of `value`:

  * If ``value`` is an instance of `TreescopeFigure`, unwraps the
    underlying treescope part.
  * If ``value`` is a string, returns a rendering of that string.
  * If ``value`` has a ``_repr_html_`` method (but isn't an instance of
    `TreescopeFigure`), returns an embedded iframe with the given HTML
    contents.
  * Otherwise, renders the value using the default treescope renderer, but
    strips off any top-level comments / copy button annotations.

  The typical use is to provide helper constructors for containers to allow
  rendering lots of different objects in the "obvious" way.

  Args:
    value: Value to wrap.

  Returns:
    A renderable treescope part showing the value.
  """
  if isinstance(value, figures_impl.TreescopeFigure):
    return value.treescope_part
  elif isinstance(value, str):
    return basic_parts.Text(value)
  else:
    maybe_html = object_inspection.to_html(value)
    if maybe_html:
      return figures_impl.InlineBlock(
          embedded_iframe.embedded_iframe(
              maybe_html,
              fallback_in_text_mode=basic_parts.Text(object.__repr__(value)),
          )
      )
    else:
      return default_renderer.build_foldable_representation(value).renderable

