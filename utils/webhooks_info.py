
def webhooks_info(
    webhook_id: Annotated[str, typer.Argument(help="The ID of the webhook.")],
    token: TokenOpt = None,
) -> None:
    """Show full details for a single webhook."""
    api = get_hf_api(token=token)
    webhook = api.get_webhook(webhook_id)
    out.dict(webhook)

