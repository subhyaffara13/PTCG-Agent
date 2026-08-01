
def hardcoded_password_string(context):
    """**B105: Test for use of hard-coded password strings**

    The use of hard-coded passwords increases the possibility of password
    guessing tremendously. This plugin test looks for all string literals and
    checks the following conditions:

    - assigned to a variable that looks like a password
    - assigned to a dict key that looks like a password
    - assigned to a class attribute that looks like a password
    - used in a comparison with a variable that looks like a password

    Variables are considered to look like a password if they have match any one
    of:

    - "password"
    - "pass"
    - "passwd"
    - "pwd"
    - "secret"
    - "token"
    - "secrete"

    Note: this can be noisy and may generate false positives.

    **Config Options:**

    None

    :Example:

    .. code-block:: none

        >> Issue: Possible hardcoded password '(root)'
           Severity: Low   Confidence: Low
           CWE: CWE-259 (https://cwe.mitre.org/data/definitions/259.html)
           Location: ./examples/hardcoded-passwords.py:5
        4 def someFunction2(password):
        5     if password == "root":
        6         print("OK, logged in")

    .. seealso::

        - https://www.owasp.org/index.php/Use_of_hard-coded_password
        - https://cwe.mitre.org/data/definitions/259.html

    .. versionadded:: 0.9.0

    .. versionchanged:: 1.7.3
        CWE information added

    """
    node = context.node
    if isinstance(node._bandit_parent, ast.Assign):
        # looks for "candidate='some_string'"
        for targ in node._bandit_parent.targets:
            if isinstance(targ, ast.Name) and RE_CANDIDATES.search(targ.id):
                return _report(node.value)
            elif isinstance(targ, ast.Attribute) and RE_CANDIDATES.search(
                targ.attr
            ):
                return _report(node.value)

    elif (
        isinstance(node._bandit_parent, ast.Dict)
        and node in node._bandit_parent.keys
        and RE_CANDIDATES.search(node.value)
    ):
        # looks for "{'candidate': 'some_string'}"
        dict_node = node._bandit_parent
        pos = dict_node.keys.index(node)
        value_node = dict_node.values[pos]
        if isinstance(value_node, ast.Constant):
            return _report(value_node.value)

    elif isinstance(
        node._bandit_parent, ast.Subscript
    ) and RE_CANDIDATES.search(node.value):
        # Py39+: looks for "dict[candidate]='some_string'"
        # subscript -> index -> string
        assign = node._bandit_parent._bandit_parent
        if (
            isinstance(assign, ast.Assign)
            and isinstance(assign.value, ast.Constant)
            and isinstance(assign.value.value, str)
        ):
            return _report(assign.value.value)

    elif isinstance(node._bandit_parent, ast.Index) and RE_CANDIDATES.search(
        node.value
    ):
        # looks for "dict[candidate]='some_string'"
        # assign -> subscript -> index -> string
        assign = node._bandit_parent._bandit_parent._bandit_parent
        if (
            isinstance(assign, ast.Assign)
            and isinstance(assign.value, ast.Constant)
            and isinstance(assign.value.value, str)
        ):
            return _report(assign.value.value)

    elif isinstance(node._bandit_parent, ast.Compare):
        # looks for "candidate == 'some_string'"
        comp = node._bandit_parent
        if isinstance(comp.left, ast.Name):
            if RE_CANDIDATES.search(comp.left.id):
                if isinstance(
                    comp.comparators[0], ast.Constant
                ) and isinstance(comp.comparators[0].value, str):
                    return _report(comp.comparators[0].value)
        elif isinstance(comp.left, ast.Attribute):
            if RE_CANDIDATES.search(comp.left.attr):
                if isinstance(
                    comp.comparators[0], ast.Constant
                ) and isinstance(comp.comparators[0].value, str):
                    return _report(comp.comparators[0].value)

