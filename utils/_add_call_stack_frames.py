
def _add_call_stack_frames(tb: types.TracebackType) -> types.TracebackType:
  # Continue up the call stack.
  #
  # We would like to avoid stepping too far up, e.g. past the exec/eval point of
  # a REPL such as IPython. To that end, we stop past the first contiguous bunch
  # of module-level frames, if we reach any such frames at all. This is a
  # heuristic that might stop in advance of the REPL boundary. For example, if
  # the call stack includes module-level frames from the current module A, and
  # the current module A was imported from within a function F elsewhere, then
  # the stack trace we produce will be truncated at F's frame.
  out = tb

  reached_module_level = False
  for f, lineno in traceback.walk_stack(tb.tb_frame):
    if _ignore_known_hidden_frame(f):
      continue
    if reached_module_level and f.f_code.co_name != '<module>':
      break
    if include_frame(f):
      out = types.TracebackType(out, f, f.f_lasti, lineno)
    if f.f_code.co_name == '<module>':
      reached_module_level = True
  return out

