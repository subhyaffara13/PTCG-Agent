
def spaces_wait(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    timeout: Annotated[
        str | None,
        typer.Option(
            help="Max time to wait: int/float with s (seconds, default), m (minutes), h (hours) or d (days).",
        ),
    ] = None,
    token: TokenOpt = None,
) -> None:
    """Wait for a Space to finish building/starting.

    Blocks until the Space leaves an intermediate stage (BUILDING, APP_STARTING, etc.)
    and reaches a settled stage. Exits with code 0 if the Space is RUNNING,
    or a non-zero exit code otherwise (e.g. BUILD_ERROR, RUNTIME_ERROR).
    """
    timeout_secs = parse_duration(timeout) if timeout is not None else None
    api = get_hf_api(token=token)
    status = out.status("Waiting for Space to be ready...")
    try:
        runtime = api.wait_for_space(space_id, timeout=timeout_secs)
    except TimeoutError:
        status.done("Timed out.")
        raise CLIError(f"Timed out after {timeout} waiting for Space '{space_id}' to be ready.") from None
    status.done(f"Space reached stage '{runtime.stage}'.")
    if runtime.stage != SpaceStage.RUNNING:
        raise CLIError(f"Space '{space_id}' is not running (stage='{runtime.stage}').")
    out.result("Space ready", space_id=space_id, stage=str(runtime.stage))
    out.hint(f"Use `hf spaces logs {space_id}` to view run logs.")

