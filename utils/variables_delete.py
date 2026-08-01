
def variables_delete(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    key: Annotated[str, typer.Argument(help="Name of the variable to remove.")],
    yes: Annotated[
        bool,
        typer.Option(
            "-y",
            "--yes",
            help="Answer Yes to prompt automatically.",
        ),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Remove an environment variable from a Space."""
    out.confirm(
        f"You are about to remove variable '{key}' from Space '{space_id}'. Proceed?",
        yes=yes,
    )
    api = get_hf_api(token=token)
    api.delete_space_variable(space_id, key=key)
    out.result("Variable deleted", space_id=space_id, key=key)
    out.hint(f"Use `hf spaces variables ls {space_id}` to list remaining variables for a Space.")

