
def dev_mode(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    stop: Annotated[bool, typer.Option(help="Stop dev mode.")] = False,
    token: TokenOpt = None,
):
    """
    Enable or disable dev mode on a Space.

    Spaces Dev Mode eases the debugging of your application and makes iterating on Spaces faster by allowing you to
    restart your application without stopping the Space container itself. This feature is available as part of a PRO
    or Team & Enterprise plan.

    See docs: https://huggingface.co/docs/hub/spaces-dev-mode
    """
    api = get_hf_api(token=token)
    if stop:
        api.disable_space_dev_mode(space_id)
        print(f"Dev mode disabled for '{space_id}'")
        return
    api.enable_space_dev_mode(space_id)
    runtime = api.wait_for_space(space_id)
    if runtime.stage != SpaceStage.RUNNING:
        out.warning(f"Dev mode is not ready (stage='{runtime.stage}')")
        return
    info = api.space_info(space_id)
    folder = getattr(info.card_data, "dev-mode-folder", "" if info.sdk == "docker" else "/home/user/app")
    folder_query_param = f"folder={folder}" if folder else ""
    print("Connect to dev environment:")
    print("")
    print("Web:")
    vscode_web_url = f"https://huggingface.co/spaces/{info.id}/dev-mode/vscode-web"
    if folder_query_param:
        vscode_web_url += f"?{folder_query_param}"
    ssh_host = f"{info.subdomain}@ssh.hf.space"
    print(f"  * VSCode: {vscode_web_url}")
    print("")
    print("Local:")
    print("1. Add your SSH key to https://huggingface.co/settings/keys")
    print(f"2. SSH with `hf spaces ssh {space_id}` (or `ssh -i <your_key> {ssh_host}`)")
    print("   Or open")
    print(f"  * VSCode: vscode://vscode-remote/ssh-remote+{ssh_host}{folder}")
    print(f"  * Cursor: cursor://vscode-remote/ssh-remote+{ssh_host}{folder}")
    print("")
    print("PS: Dev mode stops after 48h of inactivity, don't forget to save your changes regularly.")

