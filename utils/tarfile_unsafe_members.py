
def tarfile_unsafe_members(context):
    if all(
        [
            context.is_module_imported_exact("tarfile"),
            "extractall" in context.call_function_name,
        ]
    ):
        if "filter" in context.call_keywords and is_filter_data(context):
            return None
        if "members" in context.call_keywords:
            members = get_members_value(context)
            if "Function" in members:
                return exec_issue(bandit.LOW, members)
            else:
                return exec_issue(bandit.MEDIUM, members)
        return exec_issue(bandit.HIGH)

