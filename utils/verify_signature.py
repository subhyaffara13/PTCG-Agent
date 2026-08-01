
def verify_signature(message, signature, certs, verifier_cls=rsa.RSAVerifier):
    """Verify an RSA or ECDSA cryptographic signature.

    Checks that the provided ``signature`` was generated from ``bytes`` using
    the private key associated with the ``cert``.

    Args:
        message (Union[str, bytes]): The plaintext message.
        signature (Union[str, bytes]): The cryptographic signature to check.
        certs (Union[Sequence, str, bytes]): The certificate or certificates
            to use to check the signature.
        verifier_cls (Optional[~google.auth.crypt.base.Signer]): Which verifier
            class to use for verification. This can be used to select different
            algorithms, such as RSA or ECDSA. Default value is :class:`RSAVerifier`.

    Returns:
        bool: True if the signature is valid, otherwise False.
    """
    if isinstance(certs, (str, bytes)):
        certs = [certs]

    for cert in certs:
        verifier = verifier_cls.from_string(cert)
        if verifier.verify(message, signature):
            return True
    return False

