
def ssl_with_bad_defaults(context, config):
    """**B503: Test for SSL use with bad defaults specified**

    This plugin is part of a family of tests that detect the use of known bad
    versions of SSL/TLS, please see :doc:`../plugins/ssl_with_bad_version` for
    a complete discussion. Specifically, this plugin test scans for Python
    methods with default parameter values that specify the use of broken
    SSL/TLS protocol versions. Currently, detection supports methods using
    Python's native SSL/TLS support and the pyOpenSSL module. A MEDIUM severity
    warning will be reported whenever known broken protocol versions are
    detected.

    **Config Options:**

    This test shares the configuration provided for the standard
    :doc:`../plugins/ssl_with_bad_version` test, please refer to its
    documentation.

    :Example:

    .. code-block:: none

        >> Issue: Function definition identified with insecure SSL/TLS protocol
        version by default, possible security issue.
           Severity: Medium   Confidence: Medium
           CWE: CWE-327 (https://cwe.mitre.org/data/definitions/327.html)
           Location: ./examples/ssl-insecure-version.py:28
        27
        28  def open_ssl_socket(version=SSL.SSLv2_METHOD):
        29      pass

    .. seealso::

     - :func:`ssl_with_bad_version`
     - :func:`ssl_with_no_version`
     - https://heartbleed.com/
     - https://en.wikipedia.org/wiki/POODLE
     - https://security.openstack.org/guidelines/dg_move-data-securely.html

    .. versionadded:: 0.9.0

    .. versionchanged:: 1.7.3
        CWE information added

    .. versionchanged:: 1.7.5
        Added TLS 1.1

    """

    bad_ssl_versions = get_bad_proto_versions(config)
    for default in context.function_def_defaults_qual:
        val = default.split(".")[-1]
        if val in bad_ssl_versions:
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.MEDIUM,
                cwe=issue.Cwe.BROKEN_CRYPTO,
                text="Function definition identified with insecure SSL/TLS "
                "protocol version by default, possible security "
                "issue.",
            )

