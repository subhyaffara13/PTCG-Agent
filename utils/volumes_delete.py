
def volumes_delete(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
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
    """Remove all volumes from a Space."""
    out.confirm(f"You are about to remove all volumes from Space '{space_id}'. Proceed?", yes=yes)
    api = get_hf_api(token=token)
    api.delete_space_volumes(space_id)
    out.result("Volumes deleted", space_id=space_id)
    out.hint(
        f"Use `hf spaces volumes set {space_id} -v hf://<repo_type>/<repo_id>:/<mount_path>` to set volumes for a Space."
    )

