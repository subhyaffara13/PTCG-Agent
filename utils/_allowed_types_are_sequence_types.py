
def _allowed_types_are_sequence_types(allowed_types: Iterable[ir.TypeProtocol]) -> bool:
    """Check if all allowed types are Sequence types."""
    return all(isinstance(t, ir.SequenceType) for t in allowed_types)

