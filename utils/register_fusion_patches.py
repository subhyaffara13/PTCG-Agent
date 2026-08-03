from typing import Any

def register_fusion_patches(
    cls: "type[PreTrainedModel]", config, fusion_config: Mapping[str, bool | Mapping[str, Any]] | None = None
) -> None:
    """Register requested runtime fusions for `cls`.

    This function:
    - validates `fusion_config` against `_FUSION_REGISTRY`
    - resolves the enabled fusion families in user order
    - registers monkey patches and checkpoint transforms before model instantiation
    """

    if not fusion_config:
        return

    for fusion_name in _iter_enabled_fusions(fusion_config):
        _register_module_fusion(cls, config, fusion_name, _FUSION_REGISTRY[fusion_name])

