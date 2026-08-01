
def evaluate_side_effect_factory(
    side_effect_values: list[dict[str, float]],
) -> Generator[dict[str, float], None, None]:
    """
    Function that returns side effects for the _evaluate method.
    Used when we're unsure of exactly how many times _evaluate will be called.
    """
    yield from side_effect_values

    while True:
        yield side_effect_values[-1]

