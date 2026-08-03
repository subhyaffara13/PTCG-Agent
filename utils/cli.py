from typing import Any, Optional

def cli(ctx: click.Context, file: Any, quote: Any, export: Any) -> None:
    """This script is used to set, get or unset values from a .env file."""
    ctx.obj = {"QUOTE": quote, "EXPORT": export, "FILE": file}


def cli(ctx: click.Context, base_url: str, api_key: Optional[str]) -> None:
    """LiteLLM Proxy CLI - Manage your LiteLLM proxy server"""
    ctx.ensure_object(dict)

    # If no API key provided via flag or environment variable, try to load from saved token.
    # Pass base_url so we only use the stored key when it was issued for this server.
    if api_key is None:
        api_key = get_stored_api_key(expected_base_url=base_url)

    ctx.obj["base_url"] = base_url
    ctx.obj["api_key"] = api_key

    # If no subcommand was invoked, start interactive mode
    if ctx.invoked_subcommand is None:
        interactive_shell(ctx)

