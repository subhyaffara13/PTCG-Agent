
def _strip_tracer(tracer_type, tag, x):
   if isinstance(x, tracer_type) and x._trace.tag is tag:
     return x.primal
   else:
     return x

