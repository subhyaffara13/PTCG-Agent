
def weak_cryptographic_key(context, config):
    return _weak_crypto_key_size_cryptography_io(
        context, config
    ) or _weak_crypto_key_size_pycrypto(context, config)

