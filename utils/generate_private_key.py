
def generate_private_key(
    key_size: int, backend: typing.Any = None
) -> DSAPrivateKey:
    parameters = generate_parameters(key_size)
    return parameters.generate_private_key()


def generate_private_key(
    public_exponent: int,
    key_size: int,
    backend: typing.Any = None,
) -> RSAPrivateKey:
    _verify_rsa_parameters(public_exponent, key_size)
    return rust_openssl.rsa.generate_private_key(public_exponent, key_size)

