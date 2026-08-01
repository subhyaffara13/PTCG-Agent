
def _get_pubkey_hash(certificate):
    pubkey = certificate.public_key()

    # https://stackoverflow.com/a/46309453/600498
    if isinstance(pubkey, RSAPublicKey):
        h = pubkey.public_bytes(Encoding.DER, PublicFormat.PKCS1)
    elif isinstance(pubkey, EllipticCurvePublicKey):
        h = pubkey.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
    else:
        h = pubkey.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)

    sha1 = Hash(SHA1(), backend=backends.default_backend())
    sha1.update(h)
    return sha1.finalize()

