
def emit_messages(options: Options, messages: list[str], dt: float, serious: bool = False) -> None:
    # ... you know, just in case.
    if options.junit_xml:
        py_version = f"{options.python_version[0]}_{options.python_version[1]}"
        write_junit_xml(
            dt,
            serious,
            {None: messages} if messages else {},
            options.junit_xml,
            py_version,
            options.platform,
        )
    if messages:
        print("\n".join(messages))

