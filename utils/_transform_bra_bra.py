
def _transform_bra_bra(a, b):
    """Raise a TypeError if a user tries to multiply two bras.

    Multiplication based on `*` is not a shorthand for tensor products.
    """
    raise TypeError(
        'Multiplication of two bras is not allowed. Use TensorProduct instead.'
    )

