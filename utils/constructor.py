
def constructor(request):
    return request.param


def constructor(request):
    """Fixture returning parametrized IntegerArray from given sequence.

    Used to test dtype conversions.
    """
    return request.param


def constructor(request):
    """
    Fixture for testing both interval container classes.
    """
    return request.param

