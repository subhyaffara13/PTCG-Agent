
def _transform_tp_bra(a, b):
    """Raise a TypeError if a user tries to multiply TensorProduct(*bras)*bra.

    Multiplication based on `*` is not a shorthand for tensor products.
    """
    if a.kind == BraKind:
        raise TypeError(
            'Multiplication of TensorProduct(*bras)*bra is invalid.'
        )

