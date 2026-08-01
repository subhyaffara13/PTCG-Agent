
def philox_rand_offset_meta(
    shape: torch.Size,
):
    return _prims.TensorLike(torch.tensor(0, dtype=torch.int64))

