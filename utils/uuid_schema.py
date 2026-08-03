from typing import Any

def uuid_schema(
    *,
    version: Literal[1, 3, 4, 5, 6, 7, 8] | None = None,
    strict: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> UuidSchema:
    return _dict_not_none(
        type='uuid', version=version, strict=strict, ref=ref, metadata=metadata, serialization=serialization
    )

