
def setup_docs(
    functorch_api: Callable[..., Any],
    torch_func_api: Callable[..., Any] | None = None,
    new_api_name: str | None = None,
) -> None:
    api_name = functorch_api.__name__
    if torch_func_api is None:
        torch_func_api = getattr(_impl, api_name)
    # See https://docs.python.org/3/using/cmdline.html#cmdoption-OO
    if torch_func_api.__doc__ is None:
        return

    warning = get_warning(api_name, new_api_name)
    warning_note = "\n.. warning::\n\n" + textwrap.indent(warning, "    ")
    warning_note = textwrap.indent(warning_note, "    ")
    functorch_api.__doc__ = torch_func_api.__doc__ + warning_note

