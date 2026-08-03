from typing import Any

def text(
    x: float, y: float, s: str, fontdict: dict[str, Any] | None = None, **kwargs
) -> Text:
    return gca().text(x, y, s, fontdict=fontdict, **kwargs)


def text(text_content: str) -> RenderableTreePart:
  """Builds a one-line text part."""
  return Text(text_content)


def text(tag, text):
    plugin_data = SummaryMetadata.PluginData(
        plugin_name="text", content=TextPluginData(version=0).SerializeToString()
    )
    smd = SummaryMetadata(plugin_data=plugin_data)
    tensor = TensorProto(
        dtype="DT_STRING",
        string_val=[text.encode(encoding="utf_8")],
        tensor_shape=TensorShapeProto(dim=[TensorShapeProto.Dim(size=1)]),
    )
    return Summary(
        value=[Summary.Value(tag=tag + "/text_summary", metadata=smd, tensor=tensor)]
    )


def text(state: StateInline, silent: bool) -> bool:
    pos = state.pos
    posMax = state.posMax

    terminator_char = state.md.inline.terminator_re.search(state.src, pos)
    pos = terminator_char.start() if terminator_char else posMax

    if pos == state.pos:
        return False

    if not silent:
        state.pending += state.src[state.pos : pos]

    state.pos = pos

    return True


def text(x: int, y: int, message: str, fontsize: int = 16) -> str:
    return f"dt {x} {y} {fontsize} '{message}'"


def text(
    text: str,
    annotation: str | None = None,
    anchor: str | None = None,
    href: str | None = None,
) -> Doc:
  """Literal text.

  Args:
    text: The text content to be printed.
    annotation: Optional annotation for the text.
    anchor: Optional HTML anchor ID for this text. When formatted as HTML,
      wraps the text in an <a id="..."> tag.
    href: Optional HTML href for this text. When formatted as HTML,
      wraps the text in an <a href="..."> tag.
  """
  return _pretty_printer.text(text, annotation, anchor, href)  # pyrefly: ignore[bad-return]

