
def _transform_tp_ket(a, b):
    """Raise a TypeError if a user tries to multiply TensorProduct(*kets)*ket.

    Multiplication based on `*` is not a shorthand for tensor products.
    """
    if a.kind == KetKind:
        raise TypeError(
            'Multiplication of TensorProduct(*kets)*ket is invalid.'
        )

