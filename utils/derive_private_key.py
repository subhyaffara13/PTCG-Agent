
def derive_private_key(
    private_value: int,
    curve: EllipticCurve,
    backend: typing.Any = None,
) -> EllipticCurvePrivateKey:
    if not isinstance(private_value, int):
        raise TypeError("private_value must be an integer type.")

    if private_value <= 0:
        raise ValueError("private_value must be a positive integer.")

    return rust_openssl.ec.derive_private_key(private_value, curve)

