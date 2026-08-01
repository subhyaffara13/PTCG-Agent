
def cryptography_has_custom_ext() -> list[str]:
    return [
        "SSL_CTX_add_client_custom_ext",
        "SSL_CTX_add_server_custom_ext",
        "SSL_extension_supported",
    ]

