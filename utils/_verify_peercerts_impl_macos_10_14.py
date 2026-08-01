
def _verify_peercerts_impl_macos_10_14(
    ssl_context: ssl.SSLContext, sec_trust_ref: typing.Any
) -> None:
    """Verify using 'SecTrustEvaluateWithError' API for macOS 10.14+."""
    cf_error = CoreFoundation.CFErrorRef()
    sec_trust_eval_result = Security.SecTrustEvaluateWithError(
        sec_trust_ref, ctypes.byref(cf_error)
    )
    # sec_trust_eval_result is a bool (0 or 1)
    # where 1 means that the certs are trusted.
    if sec_trust_eval_result == 1:
        is_trusted = True
    elif sec_trust_eval_result == 0:
        is_trusted = False
    else:
        raise ssl.SSLError(
            f"Unknown result from Security.SecTrustEvaluateWithError: {sec_trust_eval_result!r}"
        )

    cf_error_code = 0
    if not is_trusted:
        cf_error_code = CoreFoundation.CFErrorGetCode(cf_error)

        # If the error is a known failure that we're
        # explicitly okay with from SSLContext configuration
        # we can set is_trusted accordingly.
        if ssl_context.verify_mode != ssl.CERT_REQUIRED and (
            cf_error_code == CFConst.errSecNotTrusted
            or cf_error_code == CFConst.errSecCertificateExpired
        ):
            is_trusted = True

    # If we're still not trusted then we start to
    # construct and raise the SSLCertVerificationError.
    if not is_trusted:
        cf_error_string_ref = None
        try:
            cf_error_string_ref = CoreFoundation.CFErrorCopyDescription(cf_error)

            # Can this ever return 'None' if there's a CFError?
            cf_error_message = (
                _cf_string_ref_to_str(cf_error_string_ref)
                or "Certificate verification failed"
            )

            # TODO: Not sure if we need the SecTrustResultType for anything?
            # We only care whether or not it's a success or failure for now.
            sec_trust_result_type = Security.SecTrustResultType()
            Security.SecTrustGetTrustResult(
                sec_trust_ref, ctypes.byref(sec_trust_result_type)
            )

            err = ssl.SSLCertVerificationError(cf_error_message)
            err.verify_message = cf_error_message
            err.verify_code = cf_error_code
            raise err
        finally:
            if cf_error_string_ref:
                CoreFoundation.CFRelease(cf_error_string_ref)

