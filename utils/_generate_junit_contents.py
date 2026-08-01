
def _generate_junit_contents(
    dt: float,
    serious: bool,
    messages_by_file: dict[str | None, list[str]],
    version: str,
    platform: str,
) -> str:
    from xml.sax.saxutils import escape

    if serious:
        failures = 0
        errors = len(messages_by_file)
    else:
        failures = len(messages_by_file)
        errors = 0

    xml = JUNIT_HEADER_TEMPLATE.format(
        errors=errors,
        failures=failures,
        time=dt,
        # If there are no messages, we still write one "test" indicating success.
        tests=len(messages_by_file) or 1,
    )

    if not messages_by_file:
        xml += JUNIT_TESTCASE_PASS_TEMPLATE.format(time=dt, ver=version, platform=platform)
    else:
        for filename, messages in messages_by_file.items():
            if filename is not None:
                xml += JUNIT_TESTCASE_FAIL_TEMPLATE.format(
                    text=escape("\n".join(messages)),
                    filename=filename,
                    time=dt,
                    name="mypy-py{ver}-{platform} {filename}".format(
                        ver=version, platform=platform, filename=filename
                    ),
                )
            else:
                xml += JUNIT_TESTCASE_FAIL_TEMPLATE.format(
                    text=escape("\n".join(messages)),
                    filename="mypy",
                    time=dt,
                    name=f"mypy-py{version}-{platform}",
                )

    xml += JUNIT_FOOTER

    return xml

