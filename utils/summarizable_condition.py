
def summarizable_condition(
    summary: RenderableTreePart | None = None,
    detail: RenderableTreePart | None = None,
) -> RenderableTreePart:
  """Builds a part that renders depending on combination of roundtrip/collapsed.

  The idea is that, when collapsed and not in roundtrip mode, it's sometimes
  convenient to summarize a compound node with a simpler non-roundtrippable
  representation.

  Args:
    summary: Contents to render when collapsed and not in roundtrip mode.
    detail: Contents to render when either expanded or in roundtrip mode.

  Returns:
    A renderable part that renders as ``summary`` when both collapsed and not
    in roundtrip mode, and as ``detail`` otherwise.
  """
  if summary is None:
    summary = EmptyPart()
  if detail is None:
    detail = EmptyPart()
  if not isinstance(summary, RenderableTreePart):
    raise ValueError(
        "`summary` must be a renderable part or None. Got"
        f" {type(summary).__name__}"
    )
  if not isinstance(detail, RenderableTreePart):
    raise ValueError(
        "`detail` must be a renderable part or None. Got"
        f" {type(detail).__name__}"
    )
  return SummarizableCondition(summary=summary, detail=detail)

