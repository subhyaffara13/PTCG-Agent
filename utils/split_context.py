
def split_context(ctxtag: tp.Hashable | None = None):
  ctx = current_update_context(ctxtag) if ctxtag is not None else None
  is_inner = ctx.outer_ref_outer_index is not None if ctx is not None else None
  GRAPH_CONTEXT.ref_index_stack.append(SplitContext(ctxtag, RefMap(), is_inner))

  try:
    yield GRAPH_CONTEXT.ref_index_stack[-1]
  finally:
    flatten_ctx = GRAPH_CONTEXT.ref_index_stack.pop()
    if ctxtag is not None:
      ctx = current_update_context(ctxtag)
      ctx.flatten_end(flatten_ctx.ref_index)
    del flatten_ctx.ref_index
    del flatten_ctx.ctxtag

