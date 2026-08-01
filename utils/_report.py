
def _report(value, lineno=None):
    return bandit.Issue(
        severity=bandit.LOW,
        confidence=bandit.MEDIUM,
        cwe=issue.Cwe.HARD_CODED_PASSWORD,
        text=f"Possible hardcoded password: '{value}'",
        lineno=lineno,
    )

