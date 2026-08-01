
def _get_custom_interpreter(
    implementation: str | None = None, version: str | None = None
) -> str:
    if implementation is None:
        implementation = interpreter_name()
    if version is None:
        version = interpreter_version()
    return f"{implementation}{version}"

