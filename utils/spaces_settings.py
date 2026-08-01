
def spaces_settings(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    sleep_time: Annotated[
        int | None,
        typer.Option(
            "--sleep-time",
            help="Idle time in seconds after which the Space goes to sleep. Use -1 to never sleep. Only available on upgraded hardware.",
        ),
    ] = None,
    hardware: Annotated[
        str | None,
        typer.Option(
            "--hardware",
            help="Space hardware flavor (e.g. 'cpu-basic', 't4-medium', 'l4x4'). Run 'hf spaces hardware' to list available options.",
            click_type=SoftChoice(SpaceHardware),
        ),
    ] = None,
    token: TokenOpt = None,
) -> None:
    """Update the settings of a Space."""
    api = get_hf_api(token=token)
    if hardware is not None:
        runtime = api.request_space_hardware(space_id, hardware=hardware, sleep_time=sleep_time)  # type: ignore[arg-type]
    elif sleep_time is not None:
        runtime = api.set_space_sleep_time(space_id, sleep_time=sleep_time)
    else:
        raise CLIError("Specify at least one setting to update.")
    out.result(
        "Space settings updated",
        space_id=space_id,
        hardware=runtime.requested_hardware,
        sleep_time=runtime.sleep_time,
    )
    out.hint(f"Use `hf spaces info {space_id}` to verify the runtime configuration.")

