
def setup_shell(ctx: click.Context):
    """Set up the interactive shell with banner and initial info."""
    from litellm.proxy.common_utils.banner import show_banner

    show_banner()

    # Show server connection info
    base_url = ctx.obj.get("base_url")
    click.secho(f"Connected to LiteLLM server: {base_url}\n", fg="green")

    show_commands()

