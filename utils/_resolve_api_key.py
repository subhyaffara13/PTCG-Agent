
def _resolve_api_key(ctx: click.Context) -> str:
    base_url = ctx.obj["base_url"]
    api_key = ctx.obj.get("api_key")
    if api_key:
        return api_key

    if not _is_interactive():
        raise click.ClickException(
            "No LiteLLM key found. Set LITELLM_PROXY_API_KEY (or pass --api-key) for "
            "non-interactive use, or run `lite login` from a terminal."
        )

    click.echo("No LiteLLM credentials found; starting login...")
    ctx.invoke(login)
    api_key = get_stored_api_key(expected_base_url=base_url)
    if not api_key:
        raise click.ClickException(
            "Login did not produce an API key; cannot start the agent."
        )
    return api_key

