
def make_abbreviate_selector(
    threshold: int | None, roundtrip_threshold: int | None
) -> str:
  """Builds a CSS selector that matches nodes that should be abbreviated.

  Args:
    threshold: The threshold for normal mode.
    roundtrip_threshold: The threshold for roundtrip mode.

  Returns:
    A CSS selector that matches an ancestor of any node that should be
    abbreviated.
  """
  options = []
  if threshold is not None:
    levels = f" .{ABBREVIATION_LEVEL_CLASS}" * threshold
    options.append(f"{NOT_ROUNDTRIP_SELECTOR} {COLLAPSED_SELECTOR}{levels}")
  if roundtrip_threshold is not None:
    levels = f" .{ABBREVIATION_LEVEL_CLASS}" * roundtrip_threshold
    options.append(f"{ROUNDTRIP_SELECTOR} {COLLAPSED_SELECTOR}{levels}")
  return ":is(" + ", ".join(options) + ")"

