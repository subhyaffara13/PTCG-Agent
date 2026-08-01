
def serialize_key_and_certificates(
    name: bytes | None,
    key: PKCS12PrivateKeyTypes | None,
    cert: x509.Certificate | None,
    cas: Iterable[_PKCS12CATypes] | None,
    encryption_algorithm: serialization.KeySerializationEncryption,
) -> bytes:
    if key is not None and not isinstance(
        key,
        (
            rsa.RSAPrivateKey,
            dsa.DSAPrivateKey,
            ec.EllipticCurvePrivateKey,
            ed25519.Ed25519PrivateKey,
            ed448.Ed448PrivateKey,
        ),
    ):
        raise TypeError(
            "Key must be RSA, DSA, EllipticCurve, ED25519, or ED448"
            " private key, or None."
        )

    if not isinstance(
        encryption_algorithm, serialization.KeySerializationEncryption
    ):
        raise TypeError(
            "Key encryption algorithm must be a "
            "KeySerializationEncryption instance"
        )

    if key is None and cert is None and not cas:
        raise ValueError("You must supply at least one of key, cert, or cas")

    return rust_pkcs12.serialize_key_and_certificates(
        name, key, cert, cas, encryption_algorithm
    )

