
def prep_sequence_pattern(
    seq_pattern: SequencePattern,
) -> tuple[int | None, NameExpr | None, list[Pattern]]:
    star_index: int | None = None
    capture: NameExpr | None = None
    patterns: list[Pattern] = []

    for i, pattern in enumerate(seq_pattern.patterns):
        if isinstance(pattern, StarredPattern):
            star_index = i
            capture = pattern.capture

        else:
            patterns.append(pattern)

    return star_index, capture, patterns

