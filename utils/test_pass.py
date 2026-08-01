
def test_pass(path) -> None:
    # Alias `OUTPUT_MYPY` so that it appears in the local namespace
    output_mypy = OUTPUT_MYPY

    if path not in output_mypy:
        return

    relpath = os.path.relpath(path)

    # collect any reported errors, and clean up the output
    messages = []
    for message in output_mypy[path]:
        lineno, content = _strip_filename(message)
        content = content.removeprefix("error:").lstrip()
        messages.append(f"{relpath}:{lineno} - {content}")

    if messages:
        pytest.fail("\n".join(messages), pytrace=False)

