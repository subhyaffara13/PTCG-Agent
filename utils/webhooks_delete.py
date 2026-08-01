
def webhooks_delete(
    webhook_id: Annotated[str, typer.Argument(help="The ID of the webhook to delete.")],
    yes: Annotated[
        bool,
        typer.Option(
            "--yes",
            "-y",
            help="Skip confirmation prompt.",
        ),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Delete a webhook permanently."""
    out.confirm(f"Are you sure you want to delete webhook '{webhook_id}'?", yes=yes)
    api = get_hf_api(token=token)
    api.delete_webhook(webhook_id)
    out.result("Webhook deleted", id=webhook_id)

