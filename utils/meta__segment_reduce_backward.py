
def meta__segment_reduce_backward(
    grad, output, data, reduce, lengths=None, offsets=None, axis=0, initial=None
):
    if lengths is None and offsets is None:
        raise AssertionError(
            "segment_reduce(): Either lengths or offsets must be defined"
        )
    data_contig = data.contiguous()
    grad_contig = grad.contiguous()
    return torch.empty_like(
        data_contig,
        dtype=grad_contig.dtype,
        device=grad_contig.device,
        layout=grad_contig.layout,
    )

