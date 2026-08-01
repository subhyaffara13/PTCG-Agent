
def print_response_headers(
    http_version: bytes,
    status: int,
    reason_phrase: bytes | None,
    headers: list[tuple[bytes, bytes]],
) -> None:
    console = rich.console.Console()
    http_text = format_response_headers(http_version, status, reason_phrase, headers)
    syntax = rich.syntax.Syntax(http_text, "http", theme="ansi_dark", word_wrap=True)
    console.print(syntax)
    syntax = rich.syntax.Syntax("", "http", theme="ansi_dark", word_wrap=True)
    console.print(syntax)

