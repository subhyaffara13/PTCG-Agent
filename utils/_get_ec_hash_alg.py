
def _get_ec_hash_alg(curve: ec.EllipticCurve) -> hashes.HashAlgorithm:
    if isinstance(curve, ec.SECP256R1):
        return hashes.SHA256()
    elif isinstance(curve, ec.SECP384R1):
        return hashes.SHA384()
    else:
        assert isinstance(curve, ec.SECP521R1)
        return hashes.SHA512()

