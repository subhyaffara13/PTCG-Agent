
def _weak_crypto_key_size_pycrypto(context, config):
    func_key_type = {
        "Crypto.PublicKey.DSA.generate": "DSA",
        "Crypto.PublicKey.RSA.generate": "RSA",
        "Cryptodome.PublicKey.DSA.generate": "DSA",
        "Cryptodome.PublicKey.RSA.generate": "RSA",
    }
    key_type = func_key_type.get(context.call_function_name_qual)
    if key_type:
        key_size = (
            context.get_call_arg_value("bits")
            or context.get_call_arg_at_position(0)
            or 2048
        )
        return _classify_key_size(config, key_type, key_size)

