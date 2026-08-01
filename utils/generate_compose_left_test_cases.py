
def generate_compose_left_test_cases():
    """
    Generate test cases for parametrized tests of the compose function.

    These are based on, and equivalent to, those produced by
    enerate_compose_test_cases().
    """
    return tuple(
        (tuple(reversed(compose_args)), args, kwargs, expected)
        for (compose_args, args, kwargs, expected)
        in generate_compose_test_cases()
    )

