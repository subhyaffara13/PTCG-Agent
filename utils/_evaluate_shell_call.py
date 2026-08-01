
def _evaluate_shell_call(context):
    no_formatting = isinstance(
        context.node.args[0], ast.Constant
    ) and isinstance(context.node.args[0].value, str)

    if no_formatting:
        return bandit.LOW
    else:
        return bandit.HIGH

