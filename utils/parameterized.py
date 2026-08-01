
def parameterized(harnesses: Iterable[Harness],
                  *,
                  one_containing: str | None = None,
                  include_jax_unimpl: bool = False):
  """Decorator for tests.

  The tests receive a `harness` argument.

  The `JAX_TEST_HARNESS_ONE_CONTAINING` environment variable is useful for
  debugging. If given, then picks only one harness whose name contains the
  string. The whole set of parameterized tests is reduced to one test,
  whose name is not decorated to make it easier to pick with an IDE for
  running.
  """
  one_containing = one_containing or os.environ.get(
      "JAX_TEST_HARNESS_ONE_CONTAINING")
  cases = tuple(
      # Change the testcase name to include the harness name.
      dict(
          testcase_name=harness.fullname if one_containing is None else "",
          harness=harness) for harness in harnesses if harness.filter(
              jtu.device_under_test(),
              one_containing=one_containing,
              include_jax_unimpl=include_jax_unimpl))
  if one_containing is not None:
    if not cases:
      raise ValueError(
          f"Cannot find test case with name containing {one_containing}."
          "Names are:"
          "\n".join([harness.fullname for harness in harnesses]))
    cases = cases[0:1]
  if not cases:
    # We filtered out all the harnesses.
    return jtu.skip_on_devices(jtu.device_under_test())
  return absl_parameterized.named_parameters(*cases)

