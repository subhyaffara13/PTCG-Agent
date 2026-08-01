
def spaces_pause(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    token: TokenOpt = None,
) -> None:
    """Pause a Space."""
    api = get_hf_api(token=token)
    runtime = api.pause_space(space_id)
    out.result("Space paused", space_id=space_id, stage=runtime.stage)
    out.hint(f"Use `hf spaces restart {space_id}` to restart it.")
    out.hint(
        f"Mount a Volume or bucket to persist data across restarts: `hf spaces volumes set {space_id} -v hf://...`"
    )

