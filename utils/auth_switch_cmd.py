
def auth_switch_cmd(
    token_name: Annotated[
        str | None,
        typer.Option(
            help="Name of the token to switch to",
        ),
    ] = None,
    add_to_git_credential: Annotated[
        bool,
        typer.Option(
            help="Save to git credential helper. Useful only if you plan to run git commands directly.",
        ),
    ] = False,
) -> None:
    """Switch between access tokens."""
    if token_name is None:
        token_name = _select_token_name()
    if token_name is None:
        print("No token name provided. Aborting.")
        raise typer.Exit()
    auth_switch(token_name, add_to_git_credential=add_to_git_credential)

