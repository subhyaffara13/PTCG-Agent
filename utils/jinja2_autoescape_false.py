
def jinja2_autoescape_false(context):
    # check type just to be safe
    if isinstance(context.call_function_name_qual, str):
        qualname_list = context.call_function_name_qual.split(".")
        func = qualname_list[-1]
        if "jinja2" in qualname_list and func == "Environment":
            for node in ast.walk(context.node):
                if isinstance(node, ast.keyword):
                    # definite autoescape = False
                    if getattr(node, "arg", None) == "autoescape" and (
                        getattr(node.value, "id", None) == "False"
                        or getattr(node.value, "value", None) is False
                    ):
                        return bandit.Issue(
                            severity=bandit.HIGH,
                            confidence=bandit.HIGH,
                            cwe=issue.Cwe.CODE_INJECTION,
                            text="Using jinja2 templates with autoescape="
                            "False is dangerous and can lead to XSS. "
                            "Use autoescape=True or use the "
                            "select_autoescape function to mitigate XSS "
                            "vulnerabilities.",
                        )
                    # found autoescape
                    if getattr(node, "arg", None) == "autoescape":
                        value = getattr(node, "value", None)
                        if (
                            getattr(value, "id", None) == "True"
                            or getattr(value, "value", None) is True
                        ):
                            return
                        # Check if select_autoescape function is used.
                        elif isinstance(value, ast.Call) and (
                            getattr(value.func, "attr", None)
                            == "select_autoescape"
                            or getattr(value.func, "id", None)
                            == "select_autoescape"
                        ):
                            return
                        else:
                            return bandit.Issue(
                                severity=bandit.HIGH,
                                confidence=bandit.MEDIUM,
                                cwe=issue.Cwe.CODE_INJECTION,
                                text="Using jinja2 templates with autoescape="
                                "False is dangerous and can lead to XSS. "
                                "Ensure autoescape=True or use the "
                                "select_autoescape function to mitigate "
                                "XSS vulnerabilities.",
                            )
            # We haven't found a keyword named autoescape, indicating default
            # behavior
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.CODE_INJECTION,
                text="By default, jinja2 sets autoescape to False. Consider "
                "using autoescape=True or use the select_autoescape "
                "function to mitigate XSS vulnerabilities.",
            )

