
def _chunk_cat(
    tensors: list[Tensor],
    dim: int,
    num_chunks: int,
    out: Tensor | None = None,
) -> Tensor:
    dim = _preprocess_chunk_cat_inputs(tensors, dim, num_chunks)
    padded_tensors = _pad_chunk(tensors, dim, num_chunks)
    if out is None:
        return torch.cat(padded_tensors, dim + 1)
    else:
        torch.cat(padded_tensors, dim + 1, out=out)
        return out

