
def _transform_ket_tp(a, b):
    """Raise a TypeError if a user tries to multiply ket*TensorProduct(*kets).

    Multiplication based on `*` is not a shorthand for tensor products.
    """
    if b.kind == KetKind:
        raise TypeError(
            'Multiplication of ket*TensorProduct(*kets) is invalid.'
        )

