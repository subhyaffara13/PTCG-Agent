
def _extra_classes(markup: str) -> list[str]:
    """Return the list of additional classes based on the markup."""
    if markup.startswith("?"):
        if markup.endswith("+"):
            return ["is-collapsible collapsible-open"]
        return ["is-collapsible collapsible-closed"]
    return []

