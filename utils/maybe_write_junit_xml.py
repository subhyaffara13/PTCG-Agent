
def maybe_write_junit_xml(
    td: float,
    serious: bool,
    all_messages: list[str],
    messages_by_file: dict[str | None, list[str]],
    options: Options,
) -> None:
    if options.junit_xml:
        py_version = f"{options.python_version[0]}_{options.python_version[1]}"
        if options.junit_format == "global":
            util.write_junit_xml(
                td,
                serious,
                {None: all_messages} if all_messages else {},
                options.junit_xml,
                py_version,
                options.platform,
            )
        else:
            # per_file
            util.write_junit_xml(
                td, serious, messages_by_file, options.junit_xml, py_version, options.platform
            )

