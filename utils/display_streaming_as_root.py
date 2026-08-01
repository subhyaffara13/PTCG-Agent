
def display_streaming_as_root(
    root_node: rendering_parts.RenderableTreePart,
    deferreds: Sequence[foldable_impl.DeferredWithThunk],
    roundtrip: bool = False,
    compressed: bool = True,
    stealable: bool = False,
    ignore_exceptions: bool = False,
) -> str | None:
  """Displays a root node in an IPython notebook in a streaming fashion.

  Args:
    root_node: The root node to render.
    deferreds: Deferred objects to render and splice in.
    roundtrip: Whether to render in roundtrip mode.
    compressed: Whether to compress the HTML for display.
    stealable: Whether to return an extra HTML snippet that allows the streaming
      rendering to be relocated after it is shown.
    ignore_exceptions: Whether to ignore exceptions during deferred rendering,
      replacing them with error markers.

  Returns:
    If ``stealable`` is True, a final HTML snippet which, if inserted into a
    document, will "steal" the root node rendering, moving the DOM nodes for it
    into itself. In particular, using this as the HTML rendering of the root
    node during pretty printing will correctly associate the rendering with the
    IPython "cell output", which is visible in some IPython backends (e.g.
    JupyterLab). If ``stealable`` is False, returns None.
  """
  import IPython.display  # pylint: disable=import-outside-toplevel

  render_iterator = _render_to_html_as_root_streaming(
      root_node, roundtrip, deferreds, ignore_exceptions=ignore_exceptions
  )
  encapsulated_iterator = html_encapsulation.encapsulate_streaming_html(
      render_iterator, compress=compressed, stealable=stealable
  )

  for step in encapsulated_iterator:
    if step.segment_type == html_encapsulation.SegmentType.FINAL_OUTPUT_STEALER:
      return step.html_src
    else:
      IPython.display.display(IPython.display.HTML(step.html_src))

