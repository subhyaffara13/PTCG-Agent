
def _options_enum() -> str:
    enum = """
    class Options(_IntFlag):
        OP_ALL = 1
        OP_NO_SSLv2 = 2
        OP_NO_SSLv3 = 3
        OP_NO_TLSv1 = 4
        OP_NO_TLSv1_1 = 5
        OP_NO_TLSv1_2 = 6
        OP_NO_TLSv1_3 = 7
        OP_CIPHER_SERVER_PREFERENCE = 8
        OP_SINGLE_DH_USE = 9
        OP_SINGLE_ECDH_USE = 10
        OP_NO_COMPRESSION = 11
        OP_NO_TICKET = 12
        OP_NO_RENEGOTIATION = 13
        OP_ENABLE_MIDDLEBOX_COMPAT = 14
        """
    if PY312_PLUS:
        enum += "OP_LEGACY_SERVER_CONNECT = 15"
    return enum

