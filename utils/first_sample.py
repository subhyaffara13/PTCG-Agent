
def first_sample(self: unittest.TestCase, samples: Iterable[T]) -> T:
    """
    Returns the first sample from an iterable of samples, like those returned by OpInfo.
    The test will be skipped if no samples are available.
    """
    try:
        return next(iter(samples))
    except StopIteration as e:
        raise unittest.SkipTest('Skipped! Need at least 1 sample input') from e

