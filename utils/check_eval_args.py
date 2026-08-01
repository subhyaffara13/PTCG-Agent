
def check_eval_args(args):
  for arg in args:
    if isinstance(arg, Tracer):
      raise escaped_tracer_error(arg)

