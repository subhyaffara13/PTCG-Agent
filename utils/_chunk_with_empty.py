
def _chunk_with_empty(
    tensor: torch.Tensor, num_chunks: int, dim: int
) -> list[torch.Tensor]:
    chunks = list(torch.chunk(tensor, num_chunks, dim=dim))
    while len(chunks) < num_chunks:
        chunks.append(chunks[0].new_empty(0))
    return chunks

