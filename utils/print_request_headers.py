
def print_request_headers(request: httpcore.Request, http2: bool = False) -> None:
    console = rich.console.Console()
    http_text = format_request_headers(request, http2=http2)
    syntax = rich.syntax.Syntax(http_text, "http", theme="ansi_dark", word_wrap=True)
    console.print(syntax)
    syntax = rich.syntax.Syntax("", "http", theme="ansi_dark", word_wrap=True)
    console.print(syntax)

