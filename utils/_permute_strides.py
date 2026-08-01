
def _permute_strides(out: torch.Tensor, query_strides: tuple[int, ...]) -> torch.Tensor:
    """
    Create a new tensor with the same data and shape as the input,
    but with strides permuted based on the input tensor's stride order.

    Args:
        out (torch.Tensor): The output tensor of attention.
        query_strides (List[int]): The stride order of the input query tensor

    Returns:
        torch.Tensor: A new tensor with same shape and data as the input,
        but with strides permuted based on the query tensor's stride order.
    """
    from torch._inductor.ir import get_fill_order

    fill_order = get_fill_order(query_strides)
    if out.storage_offset() != 0:
        raise AssertionError(
            f"Only support storage_offset == 0, got {out.storage_offset()}"
        )
    out_strides = _construct_strides(out.shape, fill_order)

    # Attention kernels require stride[-1]=1 for efficient memory access.
    # Ensure this by moving last dim to front of fill_order if needed.
    if out_strides[-1] != 1:
        last_dim = len(out.shape) - 1
        fill_order = list(fill_order)
        fill_order.remove(last_dim)
        fill_order = [last_dim] + fill_order
        out_strides = _construct_strides(out.shape, fill_order)

    new_out = out.new_empty_strided(out.shape, out_strides)
    new_out.copy_(out)
    return new_out

