
def nest(n: int, doc: Doc) -> Doc:
  """Increases the indentation level by `n`."""
  return _pretty_printer.nest(n, doc)  # pyrefly: ignore[bad-argument-type, bad-return]

