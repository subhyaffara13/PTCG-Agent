
def new_managed_id(provider: str, raw_provider_id: str) -> str:
    """Mint a fresh managed ID for a given raw provider ID."""
    return encode(provider, str(_uuid_mod.uuid4()), raw_provider_id)

