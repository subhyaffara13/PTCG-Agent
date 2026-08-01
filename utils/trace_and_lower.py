
def trace_and_lower(work_dir, f, f_args, f_kwargs, **_):
  lowered = jax.jit(lambda *args: f(*args, **f_kwargs)).lower(*f_args)
  return (lowered, work_dir)

