
def _override_builtin_ops():
    original_max = builtins.max
    original_min = builtins.min
    original_pow = math.pow

    # pyrefly: ignore [bad-assignment]
    builtins.max = functools.partial(
        _tensor_min_max, real_callable=original_max, tensor_callable=torch.maximum
    )

    # pyrefly: ignore [bad-assignment]
    builtins.min = functools.partial(
        _tensor_min_max, real_callable=original_min, tensor_callable=torch.minimum
    )

    math.pow = lambda x, y: x**y  # type: ignore[operator]

    try:
        yield
    finally:
        builtins.max = original_max
        builtins.min = original_min
        math.pow = original_pow

