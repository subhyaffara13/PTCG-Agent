
def compile_jaxpr(work_dir, f, f_args, f_kwargs, **_):
  del work_dir
  return jax.make_jaxpr(f)(*f_args, **f_kwargs)

