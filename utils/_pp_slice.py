
def _pp_slice(context: core.JaxprPpContext, dim, slc: Slice) -> pp.Doc:
  start, size = slc.start, slc.size
  if isinstance(start, core.Var):
    start_doc = core.pp_var(start, context)
    size_doc = (
        core.pp_var(size, context) if isinstance(size, core.Var)
        else pp.text(str(size))
    )
    return pp.concat(
      [start_doc, pp.text(":"), start_doc, pp.text("+"), size_doc])
  else:
    start_str = str(start)
    if start == 0:
      start_str = ""
    if isinstance(size, core.Var):
      size_doc = core.pp_var(size, context)
      if start_str:
        return pp.text(f"{start_str}:{start_str}+") + size_doc
      else:
        return pp.concat([pp.text(":"), size_doc])
    else:
      _val = lambda x: x.val if isinstance(x, core.Literal) else x
      end = _val(start) + _val(size)
      end_str = "" if end == dim else str(end)
      return pp.text(f"{start_str}:{end_str}")

