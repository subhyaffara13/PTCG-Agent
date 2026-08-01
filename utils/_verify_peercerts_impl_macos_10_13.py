
def _verify_peercerts_impl_macos_10_13(
    ssl_context: ssl.SSLContext, sec_trust_ref: typing.Any
) -> None:
    """Verify using 'SecTrustEvaluate' API for macOS 10.13 and earlier.
    macOS 10.14 added the 'SecTrustEvaluateWithError' API.
    """
    sec_trust_result_type = Security.SecTrustResultType()
    Security.SecTrustEvaluate(sec_trust_ref, ctypes.byref(sec_trust_result_type))

    try:
        sec_trust_result_type_as_int = int(sec_trust_result_type.value)
    except (ValueError, TypeError):
        sec_trust_result_type_as_int = -1

    # Apple doesn't document these values in their own API docs.
    # See: https://github.com/xybp888/iOS-SDKs/blob/master/iPhoneOS13.0.sdk/System/Library/Frameworks/Security.framework/Headers/SecTrust.h#L84
    if (
        ssl_context.verify_mode == ssl.CERT_REQUIRED
        and sec_trust_result_type_as_int not in (1, 4)
    ):
        # Note that we're not able to ignore only hostname errors
        # for macOS 10.13 and earlier, so check_hostname=False will
        # still return an error.
        sec_trust_result_type_to_message = {
            0: "Invalid trust result type",
            # 1: "Trust evaluation succeeded",
            2: "User confirmation required",
            3: "User specified that certificate is not trusted",
            # 4: "Trust result is unspecified",
            5: "Recoverable trust failure occurred",
            6: "Fatal trust failure occurred",
            7: "Other error occurred, certificate may be revoked",
        }
        error_message = sec_trust_result_type_to_message.get(
            sec_trust_result_type_as_int,
            f"Unknown trust result: {sec_trust_result_type_as_int}",
        )

        err = ssl.SSLCertVerificationError(error_message)
        err.verify_message = error_message
        err.verify_code = sec_trust_result_type_as_int
        raise err

