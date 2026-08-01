
def _openssl_assert(ok: bool) -> None:
    if not ok:
        errors = openssl.capture_error_stack()

        raise InternalError(
            "Unknown OpenSSL error. This error is commonly encountered when "
            "another library is not cleaning up the OpenSSL error stack. If "
            "you are using cryptography with another library that uses "
            "OpenSSL try disabling it before reporting a bug. Otherwise "
            "please file an issue at https://github.com/pyca/cryptography/"
            "issues with information on how to reproduce "
            f"this. ({errors!r})",
            errors,
        )

