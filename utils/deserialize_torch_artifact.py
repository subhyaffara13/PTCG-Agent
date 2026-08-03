from typing import Any

def deserialize_torch_artifact(
    serialized: dict[str, Any] | tuple[Any, ...] | bytes,
):
    if isinstance(serialized, (dict, tuple)):
        return serialized
    if len(serialized) == 0:
        return {}
    buffer = io.BytesIO(serialized)
    buffer.seek(0)
    # weights_only=False as we want to load custom objects here (e.g. ScriptObject)
    try:
        artifact = torch.load(buffer, weights_only=True)
    except Exception as e:
        buffer.seek(0)
        artifact = torch.load(buffer, weights_only=False)
        log.warning(
            "Fallback to weights_only=False succeeded. "
            "Loaded object of type %s after initial failure: %s",
            type(artifact),
            exc_info=e,
        )
    if not isinstance(artifact, (tuple, dict)):
        raise AssertionError(f"expected tuple or dict, got {type(artifact).__name__}")
    return artifact

