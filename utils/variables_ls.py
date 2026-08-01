
def variables_ls(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    token: TokenOpt = None,
) -> None:
    """List environment variables for a Space."""
    api = get_hf_api(token=token)
    variables = api.get_space_variables(space_id)
    items = [_dataclass_to_dict(v) for v in variables.values()]
    out.table(items)
    out.hint(f"Use `hf spaces variables add {space_id} -e KEY=VALUE` to add variables to a Space.")

