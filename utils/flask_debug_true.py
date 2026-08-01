
def flask_debug_true(context):
    if context.is_module_imported_like("flask"):
        if context.call_function_name_qual.endswith(".run"):
            if context.check_call_arg_value("debug", "True"):
                return bandit.Issue(
                    severity=bandit.HIGH,
                    confidence=bandit.MEDIUM,
                    cwe=issue.Cwe.CODE_INJECTION,
                    text="A Flask app appears to be run with debug=True, "
                    "which exposes the Werkzeug debugger and allows "
                    "the execution of arbitrary code.",
                    lineno=context.get_lineno_for_call_arg("debug"),
                )

