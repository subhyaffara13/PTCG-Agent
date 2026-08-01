
def inline(
    *subfigures: Any, wrap: bool = False
) -> figures_impl.TreescopeFigure:
  """Returns a figure that arranges a set of displayable objects along a line.

  Args:
    *subfigures: Subfigures to display inline.
    wrap: Whether to wrap (insert newlines) between words at the end of a line.

  Returns:
    A figure which can be rendered in IPython or used to build more complex
    figures.
  """
  siblings = rendering_parts.siblings(
      *(treescope_part_from_display_object(subfig) for subfig in subfigures)
  )
  if wrap:
    return figures_impl.TreescopeFigure(figures_impl.AllowWordWrap(siblings))
  else:
    return figures_impl.TreescopeFigure(figures_impl.PreventWordWrap(siblings))


def inline(state: StateCore) -> None:
    """Parse inlines"""
    for token in state.tokens:
        if token.type == "inline":
            if token.children is None:
                token.children = []
            state.md.inline.parse(token.content, state.md, state.env, token.children)

