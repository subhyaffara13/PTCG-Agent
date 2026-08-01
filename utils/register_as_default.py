
def register_as_default(
    streaming: bool = True,
    compress_html: bool = True,
):
  """Registers treescope as the default IPython renderer.

  This tells IPython to use treescope as a renderer for any object
  that doesn't have a specific renderer registered with IPython directly.

  Treescope will be configured to produce an HTML representation of most
  objects that do not have their own custom renderers. It will also be
  configured to produce summaries of jax.Array in text mode. Note that due to
  the way that IPython's text prettyprinter works, we can't easily set it up
  as a fallback renderer in text mode because IPython will prefer to use
  ordinary `repr` if it exists.

  Note that this hooks into every use of ``IPython.display.display(...)``. To
  avoid messing up ordinary display objects, if the object has a _repr_html_
  method already, we defer to that. (But if it's a structure containing display
  objects, we still use treescope as normal.)

  If the root object being rendered defines the special method
  `__treescope_root_repr__`, that method will be assumed to take no arguments
  and return a representation of the root object in Treescope's intermediate
  representation. This can be used to fully customize the rendering of a
  particular type of object. (Most types should instead define
  `__treescope_repr__`, which allows the rendering to be customized at any level
  of the tree, not just the root.)

  Args:
    streaming: Whether to render in streaming mode, which immediately displays
      the structure of the output while computing more expensive leaf
      renderings. This is useful in interactive contexts, but can mess with
      other users of IPython's formatting because the final rendered HTML is
      empty.
    compress_html: Whether to zlib-compress (i.e. zip) treescope renderings to
      reduce their size when transmitted to the browser or saved into a
      notebook.

  Raises:
    RuntimeError: If IPython is not available.
  """
  if IPython is None:
    raise RuntimeError("Cannot use `register_as_default` outside of IPython.")

  ipython_display = IPython.display

  def _render_for_ipython(value):
    repr_html_method = object_inspection.safely_get_real_method(
        value, "_repr_html_"
    )
    if repr_html_method:
      # Directly call the _repr_html_ method. We need to do this because if this
      # formatter returns None, the _repr_html_ method won't be called. (The
      # _repr_html_ method is only called if no formatter for the type is
      # found, but this formatter will run for every type due to being
      # registered for `object`.)
      return repr_html_method()  # pylint: disable=protected-access

    if isinstance(value, ipython_display.DisplayObject):
      # Don't render this to HTML, since IPython already knows how to render it.
      return None

    has_ipython_format_method = any(
        object_inspection.safely_get_real_method(value, method_name)
        for method_name in ("_repr_pretty_", "_repr_mimebundle_")
    )
    has_treescope_format_method = any(
        object_inspection.safely_get_real_method(value, method_name)
        for method_name in ("__treescope_repr__", "__treescope_root_repr__")
    )
    if has_ipython_format_method and not has_treescope_format_method:
      # Don't render this with Treescope, because it already has a different
      # rendering method for a non-HTML format.
      return None

    output_stealer = _display_and_maybe_steal(
        value=value,
        ignore_exceptions=True,
        roundtrip_mode=False,
        streaming=streaming,
        compress_html=compress_html,
        stealable=True,
    )
    # Executing the above call will have already displayed the output,
    # but it may be in the wrong place (e.g. it may appear before the
    # actual "Out" marker in JupyterLab). In `stealable` mode, by returning
    # `output_stealer` as the rendering of the object, we can ensure that the
    # output is moved to the right place.
    assert output_stealer is not None
    return output_stealer

  display_formatter = IPython.get_ipython().display_formatter
  cur_html_formatter = display_formatter.formatters["text/html"]
  cur_html_formatter.for_type(object, _render_for_ipython)

  def _render_as_text_oneline(value, p, cycle):
    del cycle
    with default_renderer.using_expansion_strategy(max_height=None):
      rendering = default_renderer.render_to_text(value, ignore_exceptions=True)
    for i, line in enumerate(rendering.split("\n")):
      if i:
        p.break_()
      p.text(line)

  # Override the text formatter to render jax.Array without copying the entire
  # array.
  cur_text_formatter = display_formatter.formatters["text/plain"]
  cur_text_formatter.for_type_by_name(
      "jaxlib.xla_extension", "ArrayImpl", _render_as_text_oneline
  )

  # Make sure the HTML formatter runs first, so streaming outputs work
  # correctly.
  old_formatters = display_formatter.formatters
  display_formatter.formatters = {}
  display_formatter.formatters["text/html"] = cur_html_formatter
  for k, v in old_formatters.items():
    if k != "text/html":
      display_formatter.formatters[k] = v

  try:
    from google.colab import _reprs  # pytype: disable=import-error  # pylint: disable=import-outside-toplevel,line-too-long

    _reprs.disable_string_repr()
    try:
      _reprs.disable_ndarray_repr()
    except KeyError:
      pass
    try:
      _reprs.disable_function_repr()
    except KeyError:
      pass
  except ImportError:
    pass

