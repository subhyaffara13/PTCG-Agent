
def _reuse_ranges(num_layers: int) -> Generator[Tuple[int, int], None, None]:
    # TODO feels like something itertools might have already
    for lbound in range(num_layers):
        # Reuse of very large #s of layers is relatively unlikely
        # +2: we want sequences of at least 2
        # otData handles single-record duplication
        for ubound in range(
            lbound + 2, min(num_layers + 1, lbound + 2 + _MAX_REUSE_LEN)
        ):
            yield (lbound, ubound)

