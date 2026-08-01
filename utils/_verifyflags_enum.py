
def _verifyflags_enum() -> str:
    enum = """
    class VerifyFlags(_IntFlag):
        VERIFY_DEFAULT = 0
        VERIFY_CRL_CHECK_LEAF = 1
        VERIFY_CRL_CHECK_CHAIN = 2
        VERIFY_X509_STRICT = 3
        VERIFY_X509_TRUSTED_FIRST = 4
        VERIFY_ALLOW_PROXY_CERTS = 5
        VERIFY_X509_PARTIAL_CHAIN = 6
        """
    return enum

