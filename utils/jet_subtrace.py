
def jet_subtrace(f, tag, order, primals, series):
  with core.take_current_trace() as parent_trace:
    trace = JetTrace(tag, parent_trace, order)
    in_tracers = map(partial(JetTracer, trace), primals, series)
    with core.set_current_trace(trace):
       ans = f(*in_tracers)

    out_primals, out_terms = unzip2(map(trace.to_primal_terms_pair, ans))
    return out_primals, out_terms

