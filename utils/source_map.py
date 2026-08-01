
def source_map(doc: Doc, source: Any) -> Doc:
  """Source mapping.

  A source map associates a region of the pretty-printer's text output with a
  source location that produced it. For the purposes of the pretty printer a
  ``source`` may be any object: we require only that we can compare sources for
  equality. A text region to source object mapping can be populated as a side
  output of the ``format`` method.
  """
  return _pretty_printer.source_map(doc, source)  # pyrefly: ignore[bad-argument-type, bad-return]

