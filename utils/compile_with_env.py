
def compile_with_env(f, f_args, f_kwargs, env_flags, compiler_flags):
  with flag_env(**env_flags):
    jax.jit(lambda *args, **kwargs: f(*args, **kwargs)).lower(
        *f_args, **f_kwargs
    ).compile(compiler_flags)

