
def yaml_load(context):
    imported = context.is_module_imported_exact("yaml")
    qualname = context.call_function_name_qual
    if not imported and isinstance(qualname, str):
        return

    qualname_list = qualname.split(".")
    func = qualname_list[-1]
    if all(
        [
            "yaml" in qualname_list,
            func == "load",
            not context.check_call_arg_value("Loader", "SafeLoader"),
            not context.check_call_arg_value("Loader", "CSafeLoader"),
            not context.get_call_arg_at_position(1) == "SafeLoader",
            not context.get_call_arg_at_position(1) == "CSafeLoader",
        ]
    ):
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.HIGH,
            cwe=issue.Cwe.IMPROPER_INPUT_VALIDATION,
            text="Use of unsafe yaml load. Allows instantiation of"
            " arbitrary objects. Consider yaml.safe_load().",
            lineno=context.node.lineno,
        )

