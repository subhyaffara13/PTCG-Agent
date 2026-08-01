
def snmp_crypto_check(context):
    """**B509: Checking for weak cryptography**

    This test is for checking for the usage of insecure SNMP cryptography:
      v3 using noAuthNoPriv.

    Please update your code to use more secure versions of SNMP. For example:

    Instead of:
      `CommunityData('public', mpModel=0)`

    Use (Defaults to usmHMACMD5AuthProtocol and usmDESPrivProtocol
      `UsmUserData("securityName", "authName", "privName")`

    :Example:

    .. code-block:: none

        >> Issue: [B509:snmp_crypto_check] You should not use SNMPv3 without encryption. noAuthNoPriv & authNoPriv is insecure
           Severity: Medium CWE: CWE-319 (https://cwe.mitre.org/data/definitions/319.html) Confidence: High
           Location: examples/snmp.py:6:11
           More Info: https://bandit.readthedocs.io/en/latest/plugins/b509_snmp_crypto_check.html
        5   # SHOULD FAIL
        6   insecure = UsmUserData("securityName")
        7   # SHOULD FAIL

    .. seealso::

     - http://snmplabs.com/pysnmp/examples/hlapi/asyncore/sync/manager/cmdgen/snmp-versions.html
     - https://cwe.mitre.org/data/definitions/319.html

    .. versionadded:: 1.7.2

    .. versionchanged:: 1.7.3
        CWE information added

    """  # noqa: E501

    if context.call_function_name_qual == "pysnmp.hlapi.UsmUserData":
        if context.call_args_count < 3:
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.CLEARTEXT_TRANSMISSION,
                text="You should not use SNMPv3 without encryption. "
                "noAuthNoPriv & authNoPriv is insecure",
                lineno=context.get_lineno_for_call_arg("UsmUserData"),
            )

