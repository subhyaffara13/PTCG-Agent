
def parse_simple_color_and_pattern_spec(
    requested_color: str | tuple[str, str],
    typename_for_warning: str | None = None,
) -> tuple[str | None, str | None]:
  """Parses a background color and pattern from a user-provided color request.

  Args:
    requested_color: A color request, which is either a single CSS color or a
      tuple of outline and background colors.
    typename_for_warning: If provided, and the color is invalid, a warning will
      be issued with this typename as context.

  Returns:
    A tuple (background_color, background_pattern) that can be passed to
    the Treescope low-level representation construction functions (such as
    `build_foldable_tree_node_from_children`) that will configure it with the
    given background color and outline.
  """
  if isinstance(requested_color, str):
    background_color = requested_color
    background_pattern = None
  elif isinstance(requested_color, tuple) and len(requested_color) == 2:
    background_color = requested_color[0]
    background_pattern = (
        f"linear-gradient({requested_color[1]},{requested_color[1]})"
    )
  else:
    if typename_for_warning:
      warnings.warn(
          f"{typename_for_warning} requested an invalid color:"
          f" {requested_color} (not a string or a tuple)"
      )
    background_color = None
    background_pattern = None
  return background_color, background_pattern

