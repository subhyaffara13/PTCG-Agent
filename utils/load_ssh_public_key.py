
def load_ssh_public_key(
    data: utils.Buffer, backend: typing.Any = None
) -> SSHPublicKeyTypes:
    cert_or_key = _load_ssh_public_identity(data, _legacy_dsa_allowed=True)
    public_key: SSHPublicKeyTypes
    if isinstance(cert_or_key, SSHCertificate):
        public_key = cert_or_key.public_key()
    else:
        public_key = cert_or_key

    if isinstance(public_key, dsa.DSAPublicKey):
        warnings.warn(
            "SSH DSA keys are deprecated and will be removed in a future "
            "release.",
            utils.DeprecatedIn40,
            stacklevel=2,
        )
    return public_key

