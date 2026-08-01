
def merge_context() -> tp.Generator[MergeContext, None, None]: ...  # type: ignore[bad-return-type]


def merge_context(
  ctxtag: tp.Hashable | None, inner: bool | None
) -> tp.Generator[MergeContext, None, None]: ...  # type: ignore[bad-return-type]


def merge_context(ctxtag: tp.Hashable | None = None, inner: bool | None = None):
  GRAPH_CONTEXT.index_ref_stack.append(MergeContext(ctxtag, IndexMap(), inner))

  try:
    yield GRAPH_CONTEXT.index_ref_stack[-1]
  finally:
    unflatten_ctx = GRAPH_CONTEXT.index_ref_stack.pop()
    index_ref = unflatten_ctx.index_ref
    if ctxtag is not None:
      if inner is None:
        raise ValueError('inner_merge must be specified when using ctxtag')
      ctx = current_update_context(ctxtag)
      ctx.unflatten_end(index_ref, inner)
    del unflatten_ctx.index_ref
    del unflatten_ctx.ctxtag

