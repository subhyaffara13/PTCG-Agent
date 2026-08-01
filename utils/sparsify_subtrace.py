
def sparsify_subtrace(f, store, tag, spenv, spvalues, *bufs):
  with core.take_current_trace() as parent:
    trace = SparseTrace(parent, tag, spenv)
    with core.set_current_trace(trace):
      in_tracers = [SparseTracer(trace, spvalue=spvalue) for spvalue in spvalues]
      outs = f(*in_tracers)
      out_traces = [trace.to_sparse_tracer(out) for out in outs]
      buffers = spenv._buffers
  store.store([out._spvalue for out in out_traces])
  return buffers

