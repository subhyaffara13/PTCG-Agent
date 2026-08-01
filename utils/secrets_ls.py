
def secrets_ls(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    token: TokenOpt = None,
) -> None:
    """List secrets for a Space. Secret values are write-only and not returned."""
    api = get_hf_api(token=token)
    secrets = api.get_space_secrets(space_id)
    items = [_dataclass_to_dict(s) for s in secrets.values()]
    out.table(items)
    out.hint(f"Use `hf spaces secrets add {space_id} -s KEY=VALUE` to add secrets to a Space.")

