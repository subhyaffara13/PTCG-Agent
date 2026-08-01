
def auth_logout(
    token_name: Annotated[
        str | None,
        typer.Option(help="Name of token to logout"),
    ] = None,
) -> None:
    """Logout from a specific token."""
    logout(token_name=token_name)

