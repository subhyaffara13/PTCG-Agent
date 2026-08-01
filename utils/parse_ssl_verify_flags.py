
def parse_ssl_verify_flags(value):
    # flags are passed in as a string representation of a list,
    # e.g. VERIFY_X509_STRICT, VERIFY_X509_PARTIAL_CHAIN
    verify_flags_str = value.replace("[", "").replace("]", "")

    verify_flags = []
    for flag in verify_flags_str.split(","):
        flag = flag.strip()
        if not hasattr(VerifyFlags, flag):
            raise ValueError(f"Invalid ssl verify flag: {flag}")
        verify_flags.append(getattr(VerifyFlags, flag))
    return verify_flags


def parse_ssl_verify_flags(value):
    # flags are passed in as a string representation of a list,
    # e.g. VERIFY_X509_STRICT, VERIFY_X509_PARTIAL_CHAIN
    verify_flags_str = value.replace("[", "").replace("]", "")

    verify_flags = []
    for flag in verify_flags_str.split(","):
        flag = flag.strip()
        if not hasattr(VerifyFlags, flag):
            raise ValueError(f"Invalid ssl verify flag: {flag}")
        verify_flags.append(getattr(VerifyFlags, flag))
    return verify_flags

