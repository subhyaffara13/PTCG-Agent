
def markupsafe_markup_xss(context, config):

    qualname = context.call_function_name_qual
    if qualname not in ("markupsafe.Markup", "flask.Markup"):
        if qualname not in config.get("extend_markup_names", []):
            # not a Markup call
            return None

    args = context.node.args
    if not args or isinstance(args[0], ast.Constant):
        # both no arguments and a constant are fine
        return None

    allowed_calls = config.get("allowed_calls", [])
    if (
        allowed_calls
        and isinstance(args[0], ast.Call)
        and get_call_name(args[0], context.import_aliases) in allowed_calls
    ):
        # the argument contains a whitelisted call
        return None

    return bandit.Issue(
        severity=bandit.MEDIUM,
        confidence=bandit.HIGH,
        cwe=issue.Cwe.XSS,
        text=f"Potential XSS with ``{qualname}`` detected. Do "
        f"not use ``{context.call_function_name}`` on untrusted data.",
    )

