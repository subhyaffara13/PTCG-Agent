
def spaces_ssh(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    identity_file: SshIdentityFileOpt = None,
    dry_run: SshDryRunOpt = False,
    auto: Annotated[
        bool,
        typer.Option("--auto", help="Enable Dev Mode without prompting if not already enabled."),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """SSH into a Space's Dev Mode container.

    Requires Dev Mode to be running on the Space and your SSH public key to be registered at https://huggingface.co/settings/keys.

    See: https://huggingface.co/docs/hub/spaces-dev-mode
    """
    api = get_hf_api(token=token)
    info = api.space_info(space_id)
    if info.runtime is None or not info.runtime.dev_mode:
        out.confirm(
            f"Dev Mode is disabled on '{space_id}'. Enable it now?", yes=auto, default=True, confirm_param="--auto"
        )
        api.enable_space_dev_mode(space_id)
        runtime = api.wait_for_space(space_id)
        if runtime.stage != SpaceStage.RUNNING:
            raise CLIError(f"Space '{space_id}' is not running (stage='{runtime.stage}').")
        info = api.space_info(space_id)
    exec_ssh(f"{info.subdomain}@ssh.hf.space", identity_file=identity_file, dry_run=dry_run)

