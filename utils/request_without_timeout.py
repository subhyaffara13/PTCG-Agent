
def request_without_timeout(context):
    HTTP_VERBS = {"get", "options", "head", "post", "put", "patch", "delete"}
    HTTPX_ATTRS = {"request", "stream", "Client", "AsyncClient"} | HTTP_VERBS
    qualname = context.call_function_name_qual.split(".")[0]

    if qualname == "requests" and context.call_function_name in HTTP_VERBS:
        # check for missing timeout
        if context.check_call_arg_value("timeout") is None:
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.LOW,
                cwe=issue.Cwe.UNCONTROLLED_RESOURCE_CONSUMPTION,
                text=f"Call to {qualname} without timeout",
            )
    if (
        qualname == "requests"
        and context.call_function_name in HTTP_VERBS
        or qualname == "httpx"
        and context.call_function_name in HTTPX_ATTRS
    ):
        # check for timeout=None
        if context.check_call_arg_value("timeout", "None"):
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.LOW,
                cwe=issue.Cwe.UNCONTROLLED_RESOURCE_CONSUMPTION,
                text=f"Call to {qualname} with timeout set to None",
            )

