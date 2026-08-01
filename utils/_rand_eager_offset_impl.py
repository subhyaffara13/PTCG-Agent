
def _rand_eager_offset_impl(offset, device: torch.device) -> Tensor:
    """
    Reserve `offset` 32-bit Philox samples and return a 1-element int64 tensor
    Place-holder: will be replaced by rand_eager_offsets
    In fx_passes/replace_random.py
        fuse_offset_creation_pass()
    """
    return torch.empty(2, dtype=torch.int64, device=device)

