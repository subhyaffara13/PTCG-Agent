
def webhooks_enable(
    webhook_id: Annotated[str, typer.Argument(help="The ID of the webhook to enable.")],
    token: TokenOpt = None,
) -> None:
    """Enable a disabled webhook."""
    api = get_hf_api(token=token)
    webhook = api.enable_webhook(webhook_id)
    out.result("Webhook enabled", id=webhook.id)

