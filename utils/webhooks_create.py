
def webhooks_create(
    watch: Annotated[
        list[str],
        typer.Option(
            "--watch",
            help="Item to watch, in 'type:name' format (e.g. 'model:bert-base-uncased'). Repeatable.",
        ),
    ],
    url: Annotated[
        str | None,
        typer.Option(help="URL to send webhook payloads to. Mutually exclusive with --job-id."),
    ] = None,
    job_id: Annotated[
        str | None,
        typer.Option(
            "--job-id",
            help="ID of a Job to trigger (from job.id) instead of pinging a URL. Mutually exclusive with --url.",
        ),
    ] = None,
    domain: Annotated[
        list[WebhookDomain] | None,
        typer.Option(
            "--domain",
            help="Domain to watch: 'repo' or 'discussions'. Repeatable. Defaults to all domains.",
        ),
    ] = None,
    secret: Annotated[
        str | None,
        typer.Option(help="Optional secret used to sign webhook payloads."),
    ] = None,
    token: TokenOpt = None,
) -> None:
    """Create a new webhook.

    Provide either --url (to ping a remote server) or --job-id (to trigger a Job), but not both.
    """
    if url is not None and job_id is not None:
        raise typer.BadParameter("Provide either --url or --job-id, not both.")
    if url is None and job_id is None:
        raise typer.BadParameter("Provide either --url or --job-id.")
    api = get_hf_api(token=token)
    watched_items = _parse_watch(watch)
    domains = [d.value for d in domain] if domain else None
    webhook = api.create_webhook(url=url, job_id=job_id, watched=watched_items, domains=domains, secret=secret)  # type: ignore
    out.result("Webhook created", id=webhook.id)

