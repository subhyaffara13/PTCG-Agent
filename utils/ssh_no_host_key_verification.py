
def ssh_no_host_key_verification(context):
    if (
        context.is_module_imported_like("paramiko")
        and context.call_function_name == "set_missing_host_key_policy"
        and context.node.args
    ):
        policy_argument = context.node.args[0]

        policy_argument_value = None
        if isinstance(policy_argument, ast.Attribute):
            policy_argument_value = policy_argument.attr
        elif isinstance(policy_argument, ast.Name):
            policy_argument_value = policy_argument.id
        elif isinstance(policy_argument, ast.Call):
            if isinstance(policy_argument.func, ast.Attribute):
                policy_argument_value = policy_argument.func.attr
            elif isinstance(policy_argument.func, ast.Name):
                policy_argument_value = policy_argument.func.id

        if policy_argument_value in ["AutoAddPolicy", "WarningPolicy"]:
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.MEDIUM,
                cwe=issue.Cwe.IMPROPER_CERT_VALIDATION,
                text="Paramiko call with policy set to automatically trust "
                "the unknown host key.",
                lineno=context.get_lineno_for_call_arg(
                    "set_missing_host_key_policy"
                ),
            )

