
def _ecdsa_key_type(public_key: ec.EllipticCurvePublicKey) -> bytes:
    """Return SSH key_type and curve_name for private key."""
    curve = public_key.curve
    if curve.name not in _ECDSA_KEY_TYPE:
        raise ValueError(
            f"Unsupported curve for ssh private key: {curve.name!r}"
        )
    return _ECDSA_KEY_TYPE[curve.name]

