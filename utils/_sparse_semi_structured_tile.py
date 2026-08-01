
def _sparse_semi_structured_tile(dense):
    """
    This function computes a 2:4 sparse tile by greedily taking the largest values.

    Since we take the largest values greedily, how the sorting algorithm handles duplicates affects
    the ultimate sparsity pattern.

    Note that this function does not have the same sorting semantics as our CUDA backend,
    which is exposed via `torch._sparse_semi_structured_tile` and thus returns a different pattern.
    """

    def greedy_prune_tile(tile):
        num_kept_row = [0, 0, 0, 0]
        num_kept_col = [0, 0, 0, 0]

        for x in tile.flatten().sort(descending=True, stable=True).indices:
            r, c = x // 4, x % 4
            if num_kept_row[r] < 2 and num_kept_col[c] < 2:
                num_kept_row[r] += 1
                num_kept_col[c] += 1
            else:
                tile[r, c] = 0

    for batch in dense.unfold(0, 4, 4).unfold(1, 4, 4):
        for tile in batch:
            greedy_prune_tile(tile)

    return dense

