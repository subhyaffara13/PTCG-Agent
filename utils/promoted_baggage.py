
def promoted_baggage(
    identity: RequestIdentity,
    request_model: str | None,
    promoted_keys: tuple[str, ...],
    metadata_keys: tuple[str, ...] = DEFAULT_BAGGAGE_METADATA_KEYS,
    team_metadata_keys: tuple[str, ...] = DEFAULT_BAGGAGE_TEAM_METADATA_KEYS,
) -> dict[str, str]:
    """Identity values to write into Baggage, filtered to ``promoted_keys``.

    ``promoted_keys`` selects from ``_PROMOTABLE``; ``metadata_keys`` selects
    sub-keys of ``identity.metadata`` to promote under ``litellm.metadata.*``;
    ``team_metadata_keys`` selects sub-keys of the team's metadata to promote
    under ``litellm.team.metadata``. Empty values are dropped.
    """
    out: dict[str, str] = {}
    for key, extract in _PROMOTABLE.items():
        if key in promoted_keys:
            value = extract(identity, request_model, team_metadata_keys)
            if value:
                out[key] = value
    for meta_key in metadata_keys:
        value = identity.metadata.get(meta_key)
        if value:
            out[f"{LiteLLM.METADATA_PREFIX}{meta_key}"] = value
    return out

