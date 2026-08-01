
def fun_sourceinfo(fun: Callable) -> str:
  # See DebugInfo.fun_src_info
  while isinstance(fun, partial):
    fun = fun.func
  fun = inspect.unwrap(fun)
  try:
    filename = fun.__code__.co_filename
    lineno = fun.__code__.co_firstlineno
    return f"{fun.__name__} at {filename}:{lineno}"
  except AttributeError:
    try:
      fun_str = str(fun)
    except:
      return "<unknown>"
    # By contract, the function name has no spaces; also, we want to avoid
    # fun_sourceinfo of the form "<object Foo at 0x1234>", because it makes
    # lowering non-deterministic.
    if m := _fun_name_re.match(fun_str):
      return m.group(1)
    return "<unknown>"

