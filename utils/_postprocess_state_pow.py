
def _postprocess_state_pow(expr):
    """Handle bras and kets raised to powers.

    Under ``*`` multiplication this is invalid. Users should use a
    TensorProduct instead.
    """
    base, exp = expr.as_base_exp()
    if base.kind == KetKind or base.kind == BraKind:
        raise TypeError(
            'A bra or ket to a power is invalid, use TensorProduct instead.'
        )

