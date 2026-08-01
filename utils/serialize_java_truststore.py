
def serialize_java_truststore(
    certs: Iterable[PKCS12Certificate],
    encryption_algorithm: serialization.KeySerializationEncryption,
) -> bytes:
    if not certs:
        raise ValueError("You must supply at least one cert")

    if not isinstance(
        encryption_algorithm, serialization.KeySerializationEncryption
    ):
        raise TypeError(
            "Key encryption algorithm must be a "
            "KeySerializationEncryption instance"
        )

    return rust_pkcs12.serialize_java_truststore(certs, encryption_algorithm)

