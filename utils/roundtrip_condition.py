
def roundtrip_condition(
    roundtrip: RenderableTreePart | None = None,
    not_roundtrip: RenderableTreePart | None = None,
) -> RenderableTreePart:
  """Builds a part that renders differently in roundtrip mode.

  Args:
    roundtrip: Contents to render when rendering in round trip mode.
    not_roundtrip: Contents to render when rendering in ordinary mode.

  Returns:
    A renderable part that renders as ``roundtrip`` in roundtrip mode
    and as ``not_roundtrip`` in ordinary mode.
  """
  if roundtrip is None:
    roundtrip = EmptyPart()
  if not_roundtrip is None:
    not_roundtrip = EmptyPart()
  if not isinstance(roundtrip, RenderableTreePart):
    raise ValueError(
        "`roundtrip` must be a renderable part or None. Got"
        f" {type(roundtrip).__name__}"
    )
  if not isinstance(not_roundtrip, RenderableTreePart):
    raise ValueError(
        "`not_roundtrip` must be a renderable part or None. Got"
        f" {type(not_roundtrip).__name__}"
    )
  return RoundtripCondition(roundtrip=roundtrip, not_roundtrip=not_roundtrip)

