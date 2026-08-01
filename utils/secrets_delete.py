
def secrets_delete(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    key: Annotated[str, typer.Argument(help="Name of the secret to remove.")],
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
    """Remove a secret from a Space."""
    out.confirm(
        f"You are about to remove secret '{key}' from Space '{space_id}'. The value cannot be recovered. Proceed?",
        yes=yes,
    )
    api = get_hf_api(token=token)
    api.delete_space_secret(space_id, key=key)
    out.result("Secret deleted", space_id=space_id, key=key)
    out.hint(f"Use `hf spaces secrets add {space_id} -s {key}=<value>` to re-add a secret to a Space.")

