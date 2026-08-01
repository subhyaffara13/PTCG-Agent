
def request_with_no_cert_validation(context):
    HTTP_VERBS = {"get", "options", "head", "post", "put", "patch", "delete"}
    HTTPX_ATTRS = {"request", "stream", "Client", "AsyncClient"} | HTTP_VERBS
    qualname = context.call_function_name_qual.split(".")[0]

    if (
        qualname == "requests"
        and context.call_function_name in HTTP_VERBS
        or qualname == "httpx"
        and context.call_function_name in HTTPX_ATTRS
    ):
        if context.check_call_arg_value("verify", "False"):
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.IMPROPER_CERT_VALIDATION,
                text=f"Call to {qualname} with verify=False disabling SSL "
                "certificate checks, security issue.",
                lineno=context.get_lineno_for_call_arg("verify"),
            )

