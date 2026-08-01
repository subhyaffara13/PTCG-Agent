
def paramiko_calls(context):
    issue_text = (
        "Possible shell injection via Paramiko call, check inputs "
        "are properly sanitized."
    )
    for module in ["paramiko"]:
        if context.is_module_imported_like(module):
            if context.call_function_name in ["exec_command"]:
                return bandit.Issue(
                    severity=bandit.MEDIUM,
                    confidence=bandit.MEDIUM,
                    cwe=issue.Cwe.OS_COMMAND_INJECTION,
                    text=issue_text,
                )

