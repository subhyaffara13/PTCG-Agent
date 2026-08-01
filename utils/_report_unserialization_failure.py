
def _report_unserialization_failure(
    type_name: str, report_class: type[BaseReport], reportdict
) -> NoReturn:
    url = "https://github.com/pytest-dev/pytest/issues"
    stream = StringIO()
    pprint("-" * 100, stream=stream)
    pprint(f"INTERNALERROR: Unknown entry type returned: {type_name}", stream=stream)
    pprint(f"report_name: {report_class}", stream=stream)
    pprint(reportdict, stream=stream)
    pprint(f"Please report this bug at {url}", stream=stream)
    pprint("-" * 100, stream=stream)
    raise RuntimeError(stream.getvalue())

