
def _transform_bra_tp(a, b):
    """Raise a TypeError if a user tries to multiply bra*TensorProduct(*bras).

    Multiplication based on `*` is not a shorthand for tensor products.
    """
    if b.kind == BraKind:
        raise TypeError(
            'Multiplication of bra*TensorProduct(*bras) is invalid.'
        )

