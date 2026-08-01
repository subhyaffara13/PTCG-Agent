
def _get_ssh_key_type(key: SSHPrivateKeyTypes | SSHPublicKeyTypes) -> bytes:
    if isinstance(key, ec.EllipticCurvePrivateKey):
        key_type = _ecdsa_key_type(key.public_key())
    elif isinstance(key, ec.EllipticCurvePublicKey):
        key_type = _ecdsa_key_type(key)
    elif isinstance(key, (rsa.RSAPrivateKey, rsa.RSAPublicKey)):
        key_type = _SSH_RSA
    elif isinstance(key, (dsa.DSAPrivateKey, dsa.DSAPublicKey)):
        key_type = _SSH_DSA
    elif isinstance(
        key, (ed25519.Ed25519PrivateKey, ed25519.Ed25519PublicKey)
    ):
        key_type = _SSH_ED25519
    else:
        raise ValueError("Unsupported key type")

    return key_type

