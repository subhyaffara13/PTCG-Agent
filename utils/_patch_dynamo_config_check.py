from typing import Any

def _patch_dynamo_config_check(changes: dict[str, Any]) -> None:
    for k, v in changes.items():
        if k not in _allowed_config_patches:
            raise ValueError(
                f"patch_dynamo_config does not support patching config {k}"
            )
        if not torch._dynamo.utils.is_safe_constant(v):
            raise ValueError(
                f"patch_dynamo_config does not support patching config {k} "
                f"with non-safe-constant value {v}"
            )

