
def ssl_with_no_version(context):
    """**B504: Test for SSL use with no version specified**

    This plugin is part of a family of tests that detect the use of known bad
    versions of SSL/TLS, please see :doc:`../plugins/ssl_with_bad_version` for
    a complete discussion. Specifically, This plugin test scans for specific
    methods in Python's native SSL/TLS support and the pyOpenSSL module that
    configure the version of SSL/TLS protocol to use. These methods are known
    to provide default value that maximize compatibility, but permit use of the
    aforementioned broken protocol versions. A LOW severity warning will be
    reported whenever this is detected.

    **Config Options:**

    This test shares the configuration provided for the standard
    :doc:`../plugins/ssl_with_bad_version` test, please refer to its
    documentation.

    :Example:

    .. code-block:: none

        >> Issue: ssl.wrap_socket call with no SSL/TLS protocol version
        specified, the default SSLv23 could be insecure, possible security
        issue.
           Severity: Low   Confidence: Medium
           CWE: CWE-327 (https://cwe.mitre.org/data/definitions/327.html)
           Location: ./examples/ssl-insecure-version.py:23
        22
        23  ssl.wrap_socket()
        24

    .. seealso::

     - :func:`ssl_with_bad_version`
     - :func:`ssl_with_bad_defaults`
     - https://heartbleed.com/
     - https://en.wikipedia.org/wiki/POODLE
     - https://security.openstack.org/guidelines/dg_move-data-securely.html

    .. versionadded:: 0.9.0

    .. versionchanged:: 1.7.3
        CWE information added

    """
    if context.call_function_name_qual == "ssl.wrap_socket":
        if context.check_call_arg_value("ssl_version") is None:
            # check_call_arg_value() returns False if the argument is found
            # but does not match the supplied value (or the default None).
            # It returns None if the arg_name passed doesn't exist. This
            # tests for that (ssl_version is not specified).
            return bandit.Issue(
                severity=bandit.LOW,
                confidence=bandit.MEDIUM,
                cwe=issue.Cwe.BROKEN_CRYPTO,
                text="ssl.wrap_socket call with no SSL/TLS protocol version "
                "specified, the default SSLv23 could be insecure, "
                "possible security issue.",
                lineno=context.get_lineno_for_call_arg("ssl_version"),
            )

