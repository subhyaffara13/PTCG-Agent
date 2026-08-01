
def _check_key_padding_mask(
    key_padding_mask: torch.Tensor, src_len: int, bsz: int
) -> None:
    torch._check_with(
        AssertionError,
        key_padding_mask.shape[0] == bsz,
        lambda: f"Expected key_padded_mask.shape[0] to be {bsz}, but got {key_padding_mask.shape[0]}",
    )
    torch._check_with(
        AssertionError,
        key_padding_mask.shape[1] == src_len,
        lambda: f"Expected key_padded_mask.shape[1] to be {src_len}, but got {key_padding_mask.shape[1]}",
    )

