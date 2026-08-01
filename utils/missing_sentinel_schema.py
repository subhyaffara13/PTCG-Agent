
def missing_sentinel_schema(
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> MissingSentinelSchema:
    """Returns a schema for the `MISSING` sentinel."""

    return _dict_not_none(
        type='missing-sentinel',
        metadata=metadata,
        serialization=serialization,
    )

