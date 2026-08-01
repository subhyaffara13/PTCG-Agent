
def _summarize_exception_stack(e: BaseException) -> str:
    """Format the exception stack by showing the text of each exception."""
    causes = [e]
    while e.__cause__ is not None:
        causes.append(e.__cause__)
        e = e.__cause__
    return (
        "\n\n## Exception summary\n\n"
        + "⬆️\n".join([f"{type(e)}: {e}\n" for e in reversed(causes)])
        + "\n(Refer to the full stack trace above for more information.)"
    )

