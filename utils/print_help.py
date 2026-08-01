
def print_help() -> None:
    console = rich.console.Console()

    console.print("[bold]HTTPX :butterfly:", justify="center")
    console.print()
    console.print("A next generation HTTP client.", justify="center")
    console.print()
    console.print(
        "Usage: [bold]httpx[/bold] [cyan]<URL> [OPTIONS][/cyan] ", justify="left"
    )
    console.print()

    table = rich.table.Table.grid(padding=1, pad_edge=True)
    table.add_column("Parameter", no_wrap=True, justify="left", style="bold")
    table.add_column("Description")
    table.add_row(
        "-m, --method [cyan]METHOD",
        "Request method, such as GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD.\n"
        "[Default: GET, or POST if a request body is included]",
    )
    table.add_row(
        "-p, --params [cyan]<NAME VALUE> ...",
        "Query parameters to include in the request URL.",
    )
    table.add_row(
        "-c, --content [cyan]TEXT", "Byte content to include in the request body."
    )
    table.add_row(
        "-d, --data [cyan]<NAME VALUE> ...", "Form data to include in the request body."
    )
    table.add_row(
        "-f, --files [cyan]<NAME FILENAME> ...",
        "Form files to include in the request body.",
    )
    table.add_row("-j, --json [cyan]TEXT", "JSON data to include in the request body.")
    table.add_row(
        "-h, --headers [cyan]<NAME VALUE> ...",
        "Include additional HTTP headers in the request.",
    )
    table.add_row(
        "--cookies [cyan]<NAME VALUE> ...", "Cookies to include in the request."
    )
    table.add_row(
        "--auth [cyan]<USER PASS>",
        "Username and password to include in the request. Specify '-' for the password"
        " to use a password prompt. Note that using --verbose/-v will expose"
        " the Authorization header, including the password encoding"
        " in a trivially reversible format.",
    )

    table.add_row(
        "--proxy [cyan]URL",
        "Send the request via a proxy. Should be the URL giving the proxy address.",
    )

    table.add_row(
        "--timeout [cyan]FLOAT",
        "Timeout value to use for network operations, such as establishing the"
        " connection, reading some data, etc... [Default: 5.0]",
    )

    table.add_row("--follow-redirects", "Automatically follow redirects.")
    table.add_row("--no-verify", "Disable SSL verification.")
    table.add_row(
        "--http2", "Send the request using HTTP/2, if the remote server supports it."
    )

    table.add_row(
        "--download [cyan]FILE",
        "Save the response content as a file, rather than displaying it.",
    )

    table.add_row("-v, --verbose", "Verbose output. Show request as well as response.")
    table.add_row("--help", "Show this message and exit.")
    console.print(table)

