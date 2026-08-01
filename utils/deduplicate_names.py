
def deduplicate_names(*seqs: Iterable[str]) -> tuple[str, ...]:
    """De-duplicate the sequence of names while keeping the original order."""
    # Ideally we would use a set, but it does not preserve insertion order.
    return tuple(dict.fromkeys(name for seq in seqs for name in seq))

