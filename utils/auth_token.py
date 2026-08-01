
def auth_token() -> None:
    """Print the current access token to stdout."""
    token = get_token()
    if token is None:
        out.error("Not logged in. Run `hf auth login` first.")
        raise typer.Exit(code=1)
    print(token)
    out.hint("Run `hf auth whoami` to see which account this token belongs to.")

