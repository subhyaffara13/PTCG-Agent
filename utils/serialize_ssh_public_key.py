
def serialize_ssh_public_key(public_key: SSHPublicKeyTypes) -> bytes:
    """One-line public key format for OpenSSH"""
    if isinstance(public_key, dsa.DSAPublicKey):
        warnings.warn(
            "SSH DSA key support is deprecated and will be "
            "removed in a future release",
            utils.DeprecatedIn40,
            stacklevel=4,
        )
    key_type = _get_ssh_key_type(public_key)
    kformat = _lookup_kformat(key_type)

    f_pub = _FragList()
    f_pub.put_sshstr(key_type)
    kformat.encode_public(public_key, f_pub)

    pub = binascii.b2a_base64(f_pub.tobytes()).strip()
    return b"".join([key_type, b" ", pub])

