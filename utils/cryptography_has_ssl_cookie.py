
def cryptography_has_ssl_cookie() -> list[str]:
    return [
        "SSL_OP_COOKIE_EXCHANGE",
        "DTLS1_COOKIE_LENGTH",
        "DTLSv1_listen",
        "SSL_CTX_set_cookie_generate_cb",
        "SSL_CTX_set_cookie_verify_cb",
    ]

