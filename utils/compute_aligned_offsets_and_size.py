
def compute_aligned_offsets_and_size(types: list[RType]) -> tuple[list[int], int]:
    """Compute offsets and total size of a list of types after alignment

    Note that the types argument are types of values that are stored
    sequentially with platform default alignment.
    """
    unaligned_sizes = [compute_rtype_size(typ) for typ in types]
    alignments = [compute_rtype_alignment(typ) for typ in types]

    current_offset = 0
    offsets = []
    final_size = 0
    for i in range(len(unaligned_sizes)):
        offsets.append(current_offset)
        if i + 1 < len(unaligned_sizes):
            cur_size = unaligned_sizes[i]
            current_offset += cur_size
            next_alignment = alignments[i + 1]
            # compute aligned offset,
            # check https://en.wikipedia.org/wiki/Data_structure_alignment for more information
            current_offset = (current_offset + (next_alignment - 1)) & -next_alignment
        else:
            struct_alignment = max(alignments)
            final_size = current_offset + unaligned_sizes[i]
            final_size = (final_size + (struct_alignment - 1)) & -struct_alignment
    return offsets, final_size

