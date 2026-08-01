
def _is_has_never_check_common_name_reliable(
    openssl_version: str,
) -> bool:
    # As of May 2023, all released versions of LibreSSL fail to reject certificates with
    # only common names, see https://github.com/urllib3/urllib3/pull/3024
    is_openssl = openssl_version.startswith("OpenSSL ")

    return is_openssl


def _is_has_never_check_common_name_reliable(
    openssl_version: str,
    openssl_version_number: int,
    implementation_name: str,
    version_info: _TYPE_VERSION_INFO,
    pypy_version_info: _TYPE_VERSION_INFO | None,
) -> bool:
    # As of May 2023, all released versions of LibreSSL fail to reject certificates with
    # only common names, see https://github.com/urllib3/urllib3/pull/3024
    is_openssl = openssl_version.startswith("OpenSSL ")
    # Before fixing OpenSSL issue #14579, the SSL_new() API was not copying hostflags
    # like X509_CHECK_FLAG_NEVER_CHECK_SUBJECT, which tripped up CPython.
    # https://github.com/openssl/openssl/issues/14579
    # This was released in OpenSSL 1.1.1l+ (>=0x101010cf)
    is_openssl_issue_14579_fixed = openssl_version_number >= 0x101010CF

    return is_openssl and (
        is_openssl_issue_14579_fixed
        or _is_bpo_43522_fixed(implementation_name, version_info, pypy_version_info)
    )

