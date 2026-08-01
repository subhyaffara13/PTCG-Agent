
def _describe_njt(njt) -> str:
    contig_type = "_contig" if njt.is_contiguous() else "_noncontig"
    if njt._lengths is not None and njt._offsets is not None:
        contig_type += "_holes"
    elif njt._ragged_idx != 1:
        contig_type += "_transposed"

    cached_data = "_without_seqlen_cache"
    if njt._max_seqlen_tensor is not None:
        cached_data = "_with_seqlen_cache"

    return f"{njt.dim()}D{contig_type}{cached_data}"

