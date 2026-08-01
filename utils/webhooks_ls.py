
def webhooks_ls(
    token: TokenOpt = None,
) -> None:
    """List all webhooks for the current user."""
    api = get_hf_api(token=token)
    results = [
        {
            "id": w.id,
            "url": w.url or "(job)",
            "disabled": w.disabled,
            "domains": w.domains or [],
            "watched": [f"{wi.type}:{wi.name}" for wi in (w.watched or [])],
        }
        for w in api.list_webhooks()
    ]
    out.table(results)

