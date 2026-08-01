
def assert_sequence_equal(
    self_: Any,
    seq1: Sequence[T],
    seq2: Sequence[T],
    msg: str | None = None,
    seq_type: type[Any] | None = None,
) -> None:
    return self_.assertTrue(seq1 == seq2, msg)

