
def make_divisible(value: int, divisor: int = 8, min_value: int | None = None) -> int:
    """
    Ensure that all layers have a channel count that is divisible by `divisor`.
    """
    if min_value is None:
        min_value = divisor
    new_value = max(min_value, int(value + divisor / 2) // divisor * divisor)
    # Make sure that round down does not go down by more than 10%.
    if new_value < 0.9 * value:
        new_value += divisor
    return int(new_value)


def make_divisible(value: int, divisor: int = 8, min_value: int | None = None) -> int:
    """
    Ensure that all layers have a channel count that is divisible by `divisor`.
    """
    if min_value is None:
        min_value = divisor
    new_value = max(min_value, int(value + divisor / 2) // divisor * divisor)
    # Make sure that round down does not go down by more than 10%.
    if new_value < 0.9 * value:
        new_value += divisor
    return int(new_value)


def make_divisible(value: int, divisor: int = 8, min_value: int | None = None) -> int:
    """
    Ensure that all layers have a channel count that is divisible by `divisor`.
    """
    if min_value is None:
        min_value = divisor
    new_value = max(min_value, int(value + divisor / 2) // divisor * divisor)
    # Make sure that round down does not go down by more than 10%.
    if new_value < 0.9 * value:
        new_value += divisor
    return int(new_value)


def make_divisible(value: int, divisor: int = 8, min_value: int | None = None) -> int:
    """
    Ensure that all layers have a channel count that is divisible by `divisor`.
    """
    if min_value is None:
        min_value = divisor
    new_value = max(min_value, int(value + divisor / 2) // divisor * divisor)
    # Make sure that round down does not go down by more than 10%.
    if new_value < 0.9 * value:
        new_value += divisor
    return int(new_value)


def make_divisible(value: int, divisor: int = 8, min_value: int | None = None) -> int:
    """
    Ensure that all layers have a channel count that is divisible by `divisor`.
    """
    if min_value is None:
        min_value = divisor
    new_value = max(min_value, int(value + divisor / 2) // divisor * divisor)
    # Make sure that round down does not go down by more than 10%.
    if new_value < 0.9 * value:
        new_value += divisor
    return int(new_value)


def make_divisible(value: int, divisor: int = 8, min_value: int | None = None) -> int:
    """
    Ensure that all layers have a channel count that is divisible by `divisor`.
    """
    if min_value is None:
        min_value = divisor
    new_value = max(min_value, int(value + divisor / 2) // divisor * divisor)
    # Make sure that round down does not go down by more than 10%.
    if new_value < 0.9 * value:
        new_value += divisor
    return int(new_value)

