
def ssl_with_bad_version(context, config):
    """**B502: Test for SSL use with bad version used**

    Several highly publicized exploitable flaws have been discovered
    in all versions of SSL and early versions of TLS. It is strongly
    recommended that use of the following known broken protocol versions be
    avoided:

    - SSL v2
    - SSL v3
    - TLS v1
    - TLS v1.1

    This plugin test scans for calls to Python methods with parameters that
    indicate the used broken SSL/TLS protocol versions. Currently, detection
    supports methods using Python's native SSL/TLS support and the pyOpenSSL
    module. A HIGH severity warning will be reported whenever known broken
    protocol versions are detected.

    It is worth noting that native support for TLS 1.2 is only available in
    more recent Python versions, specifically 2.7.9 and up, and 3.x

    A note on 'SSLv23':

    Amongst the available SSL/TLS versions provided by Python/pyOpenSSL there
    exists the option to use SSLv23. This very poorly named option actually
    means "use the highest version of SSL/TLS supported by both the server and
    client". This may (and should be) a version well in advance of SSL v2 or
    v3. Bandit can scan for the use of SSLv23 if desired, but its detection
    does not necessarily indicate a problem.

    When using SSLv23 it is important to also provide flags to explicitly
    exclude bad versions of SSL/TLS from the protocol versions considered. Both
    the Python native and pyOpenSSL modules provide the ``OP_NO_SSLv2`` and
    ``OP_NO_SSLv3`` flags for this purpose.

    **Config Options:**

    .. code-block:: yaml

        ssl_with_bad_version:
            bad_protocol_versions:
                - PROTOCOL_SSLv2
                - SSLv2_METHOD
                - SSLv23_METHOD
                - PROTOCOL_SSLv3  # strict option
                - PROTOCOL_TLSv1  # strict option
                - SSLv3_METHOD    # strict option
                - TLSv1_METHOD    # strict option

    :Example:

    .. code-block:: none

        >> Issue: ssl.wrap_socket call with insecure SSL/TLS protocol version
        identified, security issue.
           Severity: High   Confidence: High
           CWE: CWE-327 (https://cwe.mitre.org/data/definitions/327.html)
           Location: ./examples/ssl-insecure-version.py:13
        12  # strict tests
        13  ssl.wrap_socket(ssl_version=ssl.PROTOCOL_SSLv3)
        14  ssl.wrap_socket(ssl_version=ssl.PROTOCOL_TLSv1)

    .. seealso::

     - :func:`ssl_with_bad_defaults`
     - :func:`ssl_with_no_version`
     - https://heartbleed.com/
     - https://en.wikipedia.org/wiki/POODLE
     - https://security.openstack.org/guidelines/dg_move-data-securely.html
     - https://cwe.mitre.org/data/definitions/327.html

    .. versionadded:: 0.9.0

    .. versionchanged:: 1.7.3
        CWE information added

    .. versionchanged:: 1.7.5
        Added TLS 1.1

    """
    bad_ssl_versions = get_bad_proto_versions(config)
    if context.call_function_name_qual == "ssl.wrap_socket":
        if context.check_call_arg_value("ssl_version", bad_ssl_versions):
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.BROKEN_CRYPTO,
                text="ssl.wrap_socket call with insecure SSL/TLS protocol "
                "version identified, security issue.",
                lineno=context.get_lineno_for_call_arg("ssl_version"),
            )
    elif context.call_function_name_qual == "pyOpenSSL.SSL.Context":
        if context.check_call_arg_value("method", bad_ssl_versions):
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.BROKEN_CRYPTO,
                text="SSL.Context call with insecure SSL/TLS protocol "
                "version identified, security issue.",
                lineno=context.get_lineno_for_call_arg("method"),
            )

    elif (
        context.call_function_name_qual != "ssl.wrap_socket"
        and context.call_function_name_qual != "pyOpenSSL.SSL.Context"
    ):
        if context.check_call_arg_value(
            "method", bad_ssl_versions
        ) or context.check_call_arg_value("ssl_version", bad_ssl_versions):
            lineno = context.get_lineno_for_call_arg(
                "method"
            ) or context.get_lineno_for_call_arg("ssl_version")
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.MEDIUM,
                cwe=issue.Cwe.BROKEN_CRYPTO,
                text="Function call with insecure SSL/TLS protocol "
                "identified, possible security issue.",
                lineno=lineno,
            )

