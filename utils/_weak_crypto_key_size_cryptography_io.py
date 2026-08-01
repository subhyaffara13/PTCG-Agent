
def _weak_crypto_key_size_cryptography_io(context, config):
    func_key_type = {
        "cryptography.hazmat.primitives.asymmetric.dsa."
        "generate_private_key": "DSA",
        "cryptography.hazmat.primitives.asymmetric.rsa."
        "generate_private_key": "RSA",
        "cryptography.hazmat.primitives.asymmetric.ec."
        "generate_private_key": "EC",
    }
    arg_position = {
        "DSA": 0,
        "RSA": 1,
        "EC": 0,
    }
    key_type = func_key_type.get(context.call_function_name_qual)
    if key_type in ["DSA", "RSA"]:
        key_size = (
            context.get_call_arg_value("key_size")
            or context.get_call_arg_at_position(arg_position[key_type])
            or 2048
        )
        return _classify_key_size(config, key_type, key_size)
    elif key_type == "EC":
        curve_key_sizes = {
            "SECT571K1": 571,
            "SECT571R1": 570,
            "SECP521R1": 521,
            "BrainpoolP512R1": 512,
            "SECT409K1": 409,
            "SECT409R1": 409,
            "BrainpoolP384R1": 384,
            "SECP384R1": 384,
            "SECT283K1": 283,
            "SECT283R1": 283,
            "BrainpoolP256R1": 256,
            "SECP256K1": 256,
            "SECP256R1": 256,
            "SECT233K1": 233,
            "SECT233R1": 233,
            "SECP224R1": 224,
            "SECP192R1": 192,
            "SECT163K1": 163,
            "SECT163R2": 163,
        }
        curve = context.get_call_arg_value("curve") or (
            len(context.call_args) > arg_position[key_type]
            and context.call_args[arg_position[key_type]]
        )
        key_size = curve_key_sizes[curve] if curve in curve_key_sizes else 224
        return _classify_key_size(config, key_type, key_size)

