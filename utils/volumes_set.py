
def volumes_set(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    volume: VolumesOpt = None,
    token: TokenOpt = None,
) -> None:
    """Set (replace) volumes for a Space."""
    volumes = parse_volumes(volume)
    if not volumes:
        raise CLIError("At least one volume must be specified with -v/--volume.")
    api = get_hf_api(token=token)
    api.set_space_volumes(space_id, volumes=volumes)
    out.result("Volumes set", space_id=space_id, volumes=[v.to_uri() for v in volumes])
    out.hint(f"Use `hf spaces volumes ls {space_id}` to list volumes for a Space.")

