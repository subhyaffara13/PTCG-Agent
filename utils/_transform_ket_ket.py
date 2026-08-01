
def _transform_ket_ket(a, b):
    """Raise a TypeError if a user tries to multiply two kets.

    Multiplication based on `*` is not a shorthand for tensor products.
    """
    raise TypeError(
        'Multiplication of two kets is not allowed. Use TensorProduct instead.'
    )

