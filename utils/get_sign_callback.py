
def get_sign_callback(signer_lib, config_file_path):
    def sign_callback(sig, sig_len, tbs, tbs_len):
        _LOGGER.debug("calling sign callback...")

        digest = _compute_sha256_digest(tbs, tbs_len)
        digestArray = ctypes.c_char * len(digest)

        # reserve 2000 bytes for the signature, shoud be more then enough.
        # RSA signature is 256 bytes, EC signature is 70~72.
        sig_holder_len = 2000
        sig_holder = ctypes.create_string_buffer(sig_holder_len)

        signature_len = signer_lib.SignForPython(
            config_file_path.encode(),  # configFilePath
            digestArray.from_buffer(bytearray(digest)),  # digest
            len(digest),  # digestLen
            sig_holder,  # sigHolder
            sig_holder_len,  # sigHolderLen
        )

        if signature_len == 0:
            # signing failed, return 0
            return 0

        sig_len[0] = signature_len
        bs = bytearray(sig_holder)
        for i in range(signature_len):
            sig[i] = bs[i]

        return 1

    return SIGN_CALLBACK_CTYPE(sign_callback)

