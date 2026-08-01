
def get_chunk_sizes(total_elems: int, chunk_size: int) -> list[int]:
    n_chunks = total_elems // chunk_size
    chunk_sizes = [chunk_size] * n_chunks
    # remainder chunk
    remainder = total_elems % chunk_size
    if remainder != 0:
        chunk_sizes.append(remainder)
    return chunk_sizes

