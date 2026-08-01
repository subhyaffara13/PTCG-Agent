
def sparsify_fun(wrapped_fun, args: list[ArrayOrSparse]):
  tag = core.TraceTag()
  spenv = SparsifyEnv()
  spvalues = arrays_to_spvalues(spenv, args)
  in_bufs = spenv._buffers
  fun, out_spvalues = sparsify_subtrace(wrapped_fun, tag, spenv, spvalues)
  out_bufs = fun.call_wrapped(*in_bufs)
  spenv = SparsifyEnv(out_bufs)
  return spvalues_to_arrays(spenv, out_spvalues())

