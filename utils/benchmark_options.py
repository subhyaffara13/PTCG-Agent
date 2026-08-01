
def benchmark_options(options_cls):
  """Decorator to associate a BenchmarkOptions subclass with a BenchmarksGenerator."""
  if not issubclass(options_cls, BenchmarkOptions):
    raise TypeError(
        "Decorating class must be a subclass of BenchmarkOptions, got"
        f" {options_cls}"
    )

  def wrapper(generator_cls):
    if not issubclass(generator_cls, BenchmarksGenerator):
      raise TypeError(
          "benchmark_options decorator can only be used on BenchmarksGenerator"
          f" subclasses, got {generator_cls}"
      )

    generator_cls.options_class = options_cls
    return generator_cls

  return wrapper

