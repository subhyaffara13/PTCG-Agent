
def collecting_deferred_renderings() -> (
    Iterator[list[foldable_impl.DeferredWithThunk]]
):
  # pylint: disable=g-doc-return-or-yield
  """Context manager that defers and collects `maybe_defer_rendering` calls.

  This context manager can be used by renderers that wish to render deferred
  objects in a streaming fashion. When used in a
  `with collecting_deferred_renderings() as deferreds:`
  expression, `deferreds` will be a list that is populated by calls to
  `maybe_defer_rendering`. This can later be passed to
  `display_streaming_as_root` to render the deferred object in a streaming
  fashion.

  Returns:
    A context manager in which `maybe_defer_rendering` calls will be deferred
    and collected into the result list.
  """
  # pylint: enable=g-doc-return-or-yield
  try:
    target = []
    with _deferrables.set_scoped(target):
      yield target
  finally:
    pass

