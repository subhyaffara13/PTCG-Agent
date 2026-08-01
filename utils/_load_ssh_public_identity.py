
def _load_ssh_public_identity(
    data: utils.Buffer,
    _legacy_dsa_allowed=False,
) -> SSHCertificate | SSHPublicKeyTypes:
    utils._check_byteslike("data", data)

    m = _SSH_PUBKEY_RC.match(data)
    if not m:
        raise ValueError("Invalid line format")
    key_type = orig_key_type = m.group(1)
    key_body = m.group(2)
    with_cert = False
    if key_type.endswith(_CERT_SUFFIX):
        with_cert = True
        key_type = key_type[: -len(_CERT_SUFFIX)]
    if key_type == _SSH_DSA and not _legacy_dsa_allowed:
        raise UnsupportedAlgorithm(
            "DSA keys aren't supported in SSH certificates"
        )
    kformat = _lookup_kformat(key_type)

    try:
        rest = memoryview(binascii.a2b_base64(key_body))
    except (TypeError, binascii.Error):
        raise ValueError("Invalid format")

    if with_cert:
        cert_body = rest
    inner_key_type, rest = _get_sshstr(rest)
    if inner_key_type != orig_key_type:
        raise ValueError("Invalid key format")
    if with_cert:
        nonce, rest = _get_sshstr(rest)
    public_key, rest = kformat.load_public(rest)
    if with_cert:
        serial, rest = _get_u64(rest)
        cctype, rest = _get_u32(rest)
        key_id, rest = _get_sshstr(rest)
        principals, rest = _get_sshstr(rest)
        valid_principals = []
        while principals:
            principal, principals = _get_sshstr(principals)
            valid_principals.append(bytes(principal))
        valid_after, rest = _get_u64(rest)
        valid_before, rest = _get_u64(rest)
        crit_options, rest = _get_sshstr(rest)
        critical_options = _parse_exts_opts(crit_options)
        exts, rest = _get_sshstr(rest)
        extensions = _parse_exts_opts(exts)
        # Get the reserved field, which is unused.
        _, rest = _get_sshstr(rest)
        sig_key_raw, rest = _get_sshstr(rest)
        sig_type, sig_key = _get_sshstr(sig_key_raw)
        if sig_type == _SSH_DSA and not _legacy_dsa_allowed:
            raise UnsupportedAlgorithm(
                "DSA signatures aren't supported in SSH certificates"
            )
        # Get the entire cert body and subtract the signature
        tbs_cert_body = cert_body[: -len(rest)]
        signature_raw, rest = _get_sshstr(rest)
        _check_empty(rest)
        inner_sig_type, sig_rest = _get_sshstr(signature_raw)
        # RSA certs can have multiple algorithm types
        if (
            sig_type == _SSH_RSA
            and inner_sig_type
            not in [_SSH_RSA_SHA256, _SSH_RSA_SHA512, _SSH_RSA]
        ) or (sig_type != _SSH_RSA and inner_sig_type != sig_type):
            raise ValueError("Signature key type does not match")
        signature, sig_rest = _get_sshstr(sig_rest)
        _check_empty(sig_rest)
        return SSHCertificate(
            nonce,
            public_key,
            serial,
            cctype,
            key_id,
            valid_principals,
            valid_after,
            valid_before,
            critical_options,
            extensions,
            sig_type,
            sig_key,
            inner_sig_type,
            signature,
            tbs_cert_body,
            orig_key_type,
            cert_body,
        )
    else:
        _check_empty(rest)
        return public_key

