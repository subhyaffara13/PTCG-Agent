
def _check_returned_jaxtypes(dbg, out_tracers):
  for i, x in enumerate(out_tracers):
    try: typeof(x)
    except TypeError:
      if (dbg and len(paths := dbg.resolve_result_paths().result_paths) > i and
          (p := paths[i].removeprefix('result'))):
        extra = f' at output component {p}'
      else:
        extra = ''
      raise TypeError(
      f"function {dbg.func_src_info} traced for {dbg.traced_for} returned a "
      f"value of type {type(x)}{extra}, which is not a valid JAX type") from None

