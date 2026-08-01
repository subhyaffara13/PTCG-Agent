
def generate_parameters(
    key_size: int, backend: typing.Any = None
) -> DSAParameters:
    if key_size not in (1024, 2048, 3072, 4096):
        raise ValueError("Key size must be 1024, 2048, 3072, or 4096 bits.")

    return rust_openssl.dsa.generate_parameters(key_size)

