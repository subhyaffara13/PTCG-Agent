
def fold_condition(
    collapsed: RenderableTreePart | None = None,
    expanded: RenderableTreePart | None = None,
) -> RenderableTreePart:
  """Builds a part that renders differently when collapsed or expanded.

  Args:
    collapsed: Contents to render when parent is collapsed.
    expanded: Contents to render when parent is expanded.

  Returns:
    A renderable part that renders as ``collapsed`` when the parent is collapsed
    and as ``expanded`` when the parent is expanded.
  """
  if collapsed is None:
    collapsed = EmptyPart()
  if expanded is None:
    expanded = EmptyPart()
  if not isinstance(collapsed, RenderableTreePart):
    raise ValueError(
        "`collapsed` must be a renderable part or None. Got"
        f" {type(collapsed).__name__}"
    )
  if not isinstance(expanded, RenderableTreePart):
    raise ValueError(
        "`expanded` must be a renderable part or None. Got"
        f" {type(expanded).__name__}"
    )
  return FoldCondition(collapsed=collapsed, expanded=expanded)

