
def _evaluate_ast(node):
    wrapper = None
    statement = ""
    str_replace = False

    if isinstance(node._bandit_parent, ast.BinOp):
        out = utils.concat_string(node, node._bandit_parent)
        wrapper = out[0]._bandit_parent
        statement = out[1]
    elif isinstance(
        node._bandit_parent, ast.Attribute
    ) and node._bandit_parent.attr in ("format", "replace"):
        statement = node.value
        # Hierarchy for "".format() is Wrapper -> Call -> Attribute -> Str
        wrapper = node._bandit_parent._bandit_parent._bandit_parent
        if node._bandit_parent.attr == "replace":
            str_replace = True
    elif hasattr(ast, "JoinedStr") and isinstance(
        node._bandit_parent, ast.JoinedStr
    ):
        substrings = [
            child
            for child in node._bandit_parent.values
            if isinstance(child, ast.Constant) and isinstance(child.value, str)
        ]
        # JoinedStr consists of list of Constant and FormattedValue
        # instances. Let's perform one test for the whole string
        # and abandon all parts except the first one to raise one
        # failed test instead of many for the same SQL statement.
        if substrings and node == substrings[0]:
            statement = "".join([str(child.value) for child in substrings])
            wrapper = node._bandit_parent._bandit_parent

    if isinstance(wrapper, ast.Call):  # wrapped in "execute" call?
        names = ["execute", "executemany"]
        name = utils.get_called_name(wrapper)
        return (name in names, statement, str_replace)
    else:
        return (False, statement, str_replace)

