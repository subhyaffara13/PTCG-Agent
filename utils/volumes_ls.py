
def volumes_ls(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    token: TokenOpt = None,
) -> None:
    """List volumes mounted in a Space."""
    api = get_hf_api(token=token)
    info = api.space_info(space_id)
    if info.runtime is None:
        raise CLIError(f"Runtime not available for Space '{space_id}'.")
    volumes = info.runtime.volumes or []
    items = [_dataclass_to_dict(v) for v in volumes]
    out.table(items)
    out.hint(
        f"Use `hf spaces volumes set {space_id} -v hf://<repo_type>/<repo_id>:/<mount_path>` to set volumes for a Space."
    )

