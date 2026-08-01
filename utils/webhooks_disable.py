
def webhooks_disable(
    webhook_id: Annotated[str, typer.Argument(help="The ID of the webhook to disable.")],
    token: TokenOpt = None,
) -> None:
    """Disable an active webhook."""
    api = get_hf_api(token=token)
    webhook = api.disable_webhook(webhook_id)
    out.result("Webhook disabled", id=webhook.id)

