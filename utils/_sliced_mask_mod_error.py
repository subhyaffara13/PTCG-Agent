
def _sliced_mask_mod_error(
    batch: Tensor,
    head: Tensor,
    token_q: Tensor,
    token_kv: Tensor,
) -> Never:
    """
    Raises helpful error when using mask_mod from a sliced BlockMask.

    After slicing a BlockMask, the mask_mod is reset and cannot be used directly.
    Users must reassign mask_mod from the original (unsliced) BlockMask.
    """
    raise RuntimeError(
        "Cannot use mask_mod from a sliced BlockMask. "
        "When you slice a BlockMask using [], the mask_mod attribute is reset. "
        "You must set it from the original BlockMask's mask_mod."
        "\n\nIncorrect usage:"
        "\n  base_mask = create_block_mask(my_mask_fn, ...)"
        "\n  sliced_mask = base_mask[:, :, block_idx]"
        "\n  sliced_mask.mask_mod = apply_offset(sliced_mask.mask_mod, offset)  # WRONG!"
        "\n\nCorrect usage:"
        "\n  base_mask = create_block_mask(my_mask_fn, ...)"
        "\n  sliced_mask = base_mask[:, :, block_idx]"
        "\n  sliced_mask.mask_mod = apply_offset(base_mask.mask_mod, offset)  # Use base_mask!"
    )

