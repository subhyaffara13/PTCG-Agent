
def _key_identifier_from_public_key(
    public_key: CertificatePublicKeyTypes,
) -> bytes:
    if isinstance(public_key, RSAPublicKey):
        data = public_key.public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.PKCS1,
        )
    elif isinstance(public_key, EllipticCurvePublicKey):
        data = public_key.public_bytes(
            serialization.Encoding.X962,
            serialization.PublicFormat.UncompressedPoint,
        )
    else:
        # This is a very slow way to do this.
        serialized = public_key.public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        data = asn1.parse_spki_for_data(serialized)

    return hashlib.sha1(data).digest()

