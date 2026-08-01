
def load_ssh_private_key(
    data: utils.Buffer,
    password: bytes | None,
    backend: typing.Any = None,
    *,
    unsafe_skip_rsa_key_validation: bool = False,
) -> SSHPrivateKeyTypes:
    """Load private key from OpenSSH custom encoding."""
    utils._check_byteslike("data", data)
    if password is not None:
        utils._check_bytes("password", password)

    m = _PEM_RC.search(data)
    if not m:
        raise ValueError("Not OpenSSH private key format")
    p1 = m.start(1)
    p2 = m.end(1)
    data = binascii.a2b_base64(memoryview(data)[p1:p2])
    if not data.startswith(_SK_MAGIC):
        raise ValueError("Not OpenSSH private key format")
    data = memoryview(data)[len(_SK_MAGIC) :]

    # parse header
    ciphername, data = _get_sshstr(data)
    kdfname, data = _get_sshstr(data)
    kdfoptions, data = _get_sshstr(data)
    nkeys, data = _get_u32(data)
    if nkeys != 1:
        raise ValueError("Only one key supported")

    # load public key data
    pubdata, data = _get_sshstr(data)
    pub_key_type, pubdata = _get_sshstr(pubdata)
    kformat = _lookup_kformat(pub_key_type)
    pubfields, pubdata = kformat.get_public(pubdata)
    _check_empty(pubdata)

    if ciphername != _NONE or kdfname != _NONE:
        ciphername_bytes = ciphername.tobytes()
        if ciphername_bytes not in _SSH_CIPHERS:
            raise UnsupportedAlgorithm(
                f"Unsupported cipher: {ciphername_bytes!r}"
            )
        if kdfname != _BCRYPT:
            raise UnsupportedAlgorithm(f"Unsupported KDF: {kdfname!r}")
        blklen = _SSH_CIPHERS[ciphername_bytes].block_len
        tag_len = _SSH_CIPHERS[ciphername_bytes].tag_len
        # load secret data
        edata, data = _get_sshstr(data)
        # see https://bugzilla.mindrot.org/show_bug.cgi?id=3553 for
        # information about how OpenSSH handles AEAD tags
        if _SSH_CIPHERS[ciphername_bytes].is_aead:
            tag = bytes(data)
            if len(tag) != tag_len:
                raise ValueError("Corrupt data: invalid tag length for cipher")
        else:
            _check_empty(data)
        _check_block_size(edata, blklen)
        salt, kbuf = _get_sshstr(kdfoptions)
        rounds, kbuf = _get_u32(kbuf)
        _check_empty(kbuf)
        ciph = _init_cipher(ciphername_bytes, password, salt.tobytes(), rounds)
        dec = ciph.decryptor()
        edata = memoryview(dec.update(edata))
        if _SSH_CIPHERS[ciphername_bytes].is_aead:
            assert isinstance(dec, AEADDecryptionContext)
            _check_empty(dec.finalize_with_tag(tag))
        else:
            # _check_block_size requires data to be a full block so there
            # should be no output from finalize
            _check_empty(dec.finalize())
    else:
        if password:
            raise TypeError(
                "Password was given but private key is not encrypted."
            )
        # load secret data
        edata, data = _get_sshstr(data)
        _check_empty(data)
        blklen = 8
        _check_block_size(edata, blklen)
    ck1, edata = _get_u32(edata)
    ck2, edata = _get_u32(edata)
    if ck1 != ck2:
        raise ValueError("Corrupt data: broken checksum")

    # load per-key struct
    key_type, edata = _get_sshstr(edata)
    if key_type != pub_key_type:
        raise ValueError("Corrupt data: key type mismatch")
    private_key, edata = kformat.load_private(
        edata,
        pubfields,
        unsafe_skip_rsa_key_validation=unsafe_skip_rsa_key_validation,
    )
    # We don't use the comment
    _, edata = _get_sshstr(edata)

    # yes, SSH does padding check *after* all other parsing is done.
    # need to follow as it writes zero-byte padding too.
    if edata != _PADDING[: len(edata)]:
        raise ValueError("Corrupt data: invalid padding")

    if isinstance(private_key, dsa.DSAPrivateKey):
        warnings.warn(
            "SSH DSA keys are deprecated and will be removed in a future "
            "release.",
            utils.DeprecatedIn40,
            stacklevel=2,
        )

    return private_key

