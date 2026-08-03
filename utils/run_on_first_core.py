import functools

def run_on_first_core(core_axis_name: str):
  """Runs a function on the first core in a given axis."""
  num_cores = jax.lax.axis_size(core_axis_name)
  if num_cores == 1:
    return lambda f: f()

  def wrapped(f):
    core_id = jax.lax.axis_index(core_axis_name)

    @pl_helpers.when(core_id == 0)
    @functools.wraps(f)
    def _():
      return f()

  return wrapped

