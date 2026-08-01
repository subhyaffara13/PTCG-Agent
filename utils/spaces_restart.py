
def spaces_restart(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    factory_reboot: Annotated[
        bool,
        typer.Option(
            "--factory-reboot",
            help="Rebuild the Space from scratch without using the build cache.",
        ),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Restart a Space."""
    api = get_hf_api(token=token)
    runtime = api.restart_space(space_id, factory_reboot=factory_reboot)
    out.result(
        "Space restart triggered",
        space_id=space_id,
        stage=runtime.stage,
        factory_reboot=factory_reboot,
    )
    out.hint(f"Use `hf spaces wait {space_id}` to wait until the Space is ready.")
    out.hint(
        f"Mount a Volume or bucket to persist data across restarts: `hf spaces volumes set {space_id} -v hf://...`"
    )

