
def exportdb_error_message(case_name: str) -> str:
    return (
        "For more information about this error, see: "
        + "https://pytorch.org/docs/main/generated/exportdb/index.html#"
        + case_name.replace("_", "-")
    )


def exportdb_error_message(case_name: str) -> str:
    from .examples import all_examples
    from torch._utils_internal import log_export_usage

    ALL_EXAMPLES = all_examples()
    # Detect whether case_name is really registered in exportdb.
    if case_name in ALL_EXAMPLES:
        url_case_name = case_name.replace("_", "-")
        return f"See {case_name} in exportdb for unsupported case. \
                https://pytorch.org/docs/main/generated/exportdb/index.html#{url_case_name}"
    else:
        log_export_usage(
            event="export.error.casenotregistered",
            message=case_name,
        )
        return f"{case_name} is unsupported."

