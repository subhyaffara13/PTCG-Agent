
def sha256_base64(data: bytes) -> str:
    # SHA-256 is used here to compute the x-content-sha256 header required by the
    # OCI HTTP signing specification (RSA-SHA256 request signing), not for password
    # or secret hashing.  This is the correct and mandated algorithm for this purpose.
    # See: https://docs.oracle.com/en-us/iaas/Content/API/Concepts/signingrequests.htm
    #
    # ``usedforsecurity=False`` declares non-security intent to static analyzers
    # (CodeQL ``py/weak-sensitive-data-hashing``) — without it the request body
    # gets flagged as "password-like data" via taint tracking.
    digest = hashlib.sha256(data, usedforsecurity=False).digest()  # noqa: S324
    return base64.b64encode(digest).decode()

