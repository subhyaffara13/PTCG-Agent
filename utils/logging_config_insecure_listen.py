
def logging_config_insecure_listen(context):
    if (
        context.call_function_name_qual == "logging.config.listen"
        and "verify" not in context.call_keywords
    ):
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.HIGH,
            cwe=issue.Cwe.CODE_INJECTION,
            text="Use of insecure logging.config.listen detected.",
        )

