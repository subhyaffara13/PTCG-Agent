
def _make_stateful_sampler(sampler: SampleFnType) -> KeylessSampleFnType:
  """Converts a jax.random sampling function to a stateful version.

  Args:
    sampler: A sampling function that consumes a key and returns
      random samples.

  Returns:
    A stateful sampling function with the key argument removed.
  """
  def new_sampler(*args, **kwargs):
    # Pass in a placeholder key into the sampling function.
    # The key is ignored by the stateful random_bits function, but all jax
    # sampling functions expect a key as input so we must pass one in here.
    placeholder_key = jax_api_random.key(0, impl=tpu_internal_stateful_impl)
    return sampler(placeholder_key, *args, **kwargs)
  # Remove key argument from docstring.
  if sampler.__doc__:
    doc_lines = filter(
        lambda line: "key:" not in line, sampler.__doc__.split("\n"))
    new_sampler.__doc__ = "\n".join(doc_lines)
  return new_sampler

