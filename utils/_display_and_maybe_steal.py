
def _display_and_maybe_steal(
    value: Any,
    ignore_exceptions: bool,
    roundtrip_mode: bool,
    streaming: bool,
    compress_html: bool,
    stealable: bool,
) -> str | None:
  """Helper to display a value, possibly with streaming and output stealing.

  Args:
    value: Value to display.
    ignore_exceptions: Whether to ignore exceptions during rendering.
    roundtrip_mode: Whether to start in roundtrip mode.
    streaming: Whether to render in streaming mode.
    compress_html: Whether to compress the HTML.
    stealable: Whether to return an HTML snippet that can be used to steal the
      output if it is already displayed.

  Returns:
    If `stealable` is True, returns an HTML snippet that can be used to steal
    the output if it is already displayed. Otherwise, returns None.
  """
  assert IPython is not None
  with contextlib.ExitStack() as stack:
    if streaming:
      deferreds = stack.enter_context(lowering.collecting_deferred_renderings())
    else:
      deferreds = []

    root_repr_method = object_inspection.safely_get_real_method(
        value, "__treescope_root_repr__"
    )
    if root_repr_method:
      foldable_ir = root_repr_method()
    else:
      foldable_ir = rendering_parts.build_full_line_with_annotations(
          default_renderer.build_foldable_representation(
              value, ignore_exceptions=ignore_exceptions
          )
      )
    if streaming:
      return lowering.display_streaming_as_root(
          foldable_ir,
          deferreds,
          roundtrip=roundtrip_mode,
          compressed=compress_html,
          stealable=stealable,
          ignore_exceptions=ignore_exceptions,
      )
    else:
      rendering = lowering.render_to_html_as_root(
          foldable_ir,
          roundtrip=roundtrip_mode,
          compressed=compress_html,
      )
      if stealable:
        return rendering
      else:
        IPython.display.display(IPython.display.HTML(rendering))

