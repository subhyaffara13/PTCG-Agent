
def assert_used(context, config):
    for skip in config.get("skips", []):
        if fnmatch.fnmatch(context.filename, skip):
            return None

    return bandit.Issue(
        severity=bandit.LOW,
        confidence=bandit.HIGH,
        cwe=issue.Cwe.IMPROPER_CHECK_OF_EXCEPT_COND,
        text=(
            "Use of assert detected. The enclosed code "
            "will be removed when compiling to optimised byte code."
        ),
    )

