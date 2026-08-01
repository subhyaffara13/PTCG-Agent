
def webhooks_update(
    webhook_id: Annotated[str, typer.Argument(help="The ID of the webhook to update.")],
    url: Annotated[
        str | None,
        typer.Option(help="New URL to send webhook payloads to."),
    ] = None,
    watch: Annotated[
        list[str] | None,
        typer.Option(
            "--watch",
            help=(
                "New list of items to watch, in 'type:name' format. "
                "Repeatable. Replaces the entire existing watched list."
            ),
        ),
    ] = None,
    domain: Annotated[
        list[WebhookDomain] | None,
        typer.Option(
            "--domain",
            help="New list of domains to watch: 'repo' or 'discussions'. Repeatable.",
        ),
    ] = None,
    secret: Annotated[
        str | None,
        typer.Option(help="New secret used to sign webhook payloads."),
    ] = None,
    token: TokenOpt = None,
) -> None:
    """Update an existing webhook. Only provided options are changed."""
    api = get_hf_api(token=token)
    watched_items = _parse_watch(watch) if watch else None
    domains = [d.value for d in domain] if domain else None
    webhook = api.update_webhook(webhook_id, url=url, watched=watched_items, domains=domains, secret=secret)  # type: ignore
    out.result("Webhook updated", id=webhook.id)

