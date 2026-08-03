import re

def rename_source_key(
    source_key: str,
    weight_renamings: list[WeightRenaming],
    weight_converters: list[WeightConverter],
    base_model_prefix: str | None = None,
    meta_state_dict: dict | None = None,
) -> tuple[str, str | None]:
    """
    Rename a checkpoint key by first applying all `WeightRenaming`s, then at most one `WeightConverter`.

    A renaming and a converter may act on the same key in that order: the renaming normalises the
    key into the namespace the converter expects. The reverse holds on the save path (converter
    first, then renaming). There is no need for a converter-then-rename order because converters
    act only on specific leaf patterns; no subsequent renamings should ever target their output.

    Args:
        source_key (`str`):
            The original checkpoint key to rename.
        weight_renamings (`list[WeightRenaming]`):
            Applied in order; every matching renaming fires (they may chain).
        weight_converters (`list[WeightConverter]`):
            Applied after all renamings; at most one may match. Subsequent converters are skipped.
        base_model_prefix (`str`, *optional*):
            Base-model prefix to add or strip when both `base_model_prefix` and `meta_state_dict` are given.
        meta_state_dict (`dict`, *optional*):
            Meta state dict used to decide whether `base_model_prefix` should be added or stripped.

    Returns:
        `tuple[str, str | None]`: The renamed key and the matched converter's source pattern
        (or `None` if no converter matched).
    """
    renamed_key = source_key
    # 1. apply all renamings in turns (if multiple match, it's the responsibility of the mappings to make sure they
    # are coherent)
    for renaming in weight_renamings:
        renamed_key, _ = renaming.rename_source_key(renamed_key)

    # 2. apply renaming through weight conversions on the key if we have any WeightConverter (here we stop after
    # the first match, as we assume only 1 converter can match any source key)
    source_pattern = None
    for converter in weight_converters:
        renamed_key, source_pattern = converter.rename_source_key(renamed_key)
        if source_pattern is not None:
            break

    # 3. check if we need to add or remove base_model_prefix if necessary (only during loading, not saving)
    if base_model_prefix is not None and meta_state_dict is not None:
        if (
            renamed_key.startswith(base_model_prefix)
            and meta_state_dict.get(re.sub(f"^{base_model_prefix}.", "", renamed_key, count=1)) is not None
        ):
            renamed_key = re.sub(f"^{base_model_prefix}.", "", renamed_key, count=1)
        elif meta_state_dict.get(f"{base_model_prefix}.{renamed_key}") is not None:
            renamed_key = f"{base_model_prefix}.{renamed_key}"

    return renamed_key, source_pattern

