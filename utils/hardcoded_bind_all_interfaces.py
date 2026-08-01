
def hardcoded_bind_all_interfaces(context):
    if context.string_val == "0.0.0.0":  # nosec: B104
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.MEDIUM,
            cwe=issue.Cwe.MULTIPLE_BINDS,
            text="Possible binding to all interfaces.",
        )

