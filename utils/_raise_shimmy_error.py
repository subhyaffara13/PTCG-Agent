
def _raise_shimmy_error(*args: Any, **kwargs: Any):
    raise ImportError(
        'To use the gym compatibility environments, run `pip install "shimmy[gym-v21]"` or `pip install "shimmy[gym-v26]"`'
    )

