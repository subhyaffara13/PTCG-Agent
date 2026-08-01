
def hardcoded_password_default(context):
    """**B107: Test for use of hard-coded password argument defaults**

    The use of hard-coded passwords increases the possibility of password
    guessing tremendously. This plugin test looks for all function definitions
    that specify a default string literal for some argument. It checks that
    the argument does not look like a password.

    Variables are considered to look like a password if they have match any one
    of:

    - "password"
    - "pass"
    - "passwd"
    - "pwd"
    - "secret"
    - "token"
    - "secrete"

    Note: this can be noisy and may generate false positives.  We do not
    report on None values which can be legitimately used as a default value,
    when initializing a function or class.

    **Config Options:**

    None

    :Example:

    .. code-block:: none

        >> Issue: [B107:hardcoded_password_default] Possible hardcoded
        password: 'Admin'
           Severity: Low   Confidence: Medium
           CWE: CWE-259 (https://cwe.mitre.org/data/definitions/259.html)
           Location: ./examples/hardcoded-passwords.py:1

        1    def someFunction(user, password="Admin"):
        2      print("Hi " + user)

    .. seealso::

        - https://www.owasp.org/index.php/Use_of_hard-coded_password
        - https://cwe.mitre.org/data/definitions/259.html

    .. versionadded:: 0.9.0

    .. versionchanged:: 1.7.3
        CWE information added

    """
    # looks for "def function(candidate='some_string')"

    # this pads the list of default values with "None" if nothing is given
    defs = [None] * (
        len(context.node.args.args) - len(context.node.args.defaults)
    )
    defs.extend(context.node.args.defaults)

    # go through all (param, value)s and look for candidates
    for key, val in zip(context.node.args.args, defs):
        if isinstance(key, (ast.Name, ast.arg)):
            # Skip if the default value is None
            if val is None or (
                isinstance(val, ast.Constant) and val.value is None
            ):
                continue
            if (
                isinstance(val, ast.Constant)
                and isinstance(val.value, str)
                and RE_CANDIDATES.search(key.arg)
            ):
                return _report(val.value)

