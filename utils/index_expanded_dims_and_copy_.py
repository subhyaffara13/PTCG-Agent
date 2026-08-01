
def index_expanded_dims_and_copy_(
    dst: torch.Tensor,
    src: torch.Tensor,
    expanded_dims: list[int],
) -> None:
    "Index into expanded dimensions of both dst and src then copy_"
    dst = index_expanded_dims(dst, expanded_dims)
    src = index_expanded_dims(src, expanded_dims)
    dst.copy_(src)

