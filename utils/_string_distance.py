
def _string_distance(seq1: str, seq2: str, seq1_length: int, seq2_length: int) -> int:
    if not seq1_length:
        return seq2_length

    if not seq2_length:
        return seq1_length

    row = [*list(range(1, seq2_length + 1)), 0]
    for seq1_index, seq1_char in enumerate(seq1):
        last_row = row
        row = [0] * seq2_length + [seq1_index + 1]

        for seq2_index, seq2_char in enumerate(seq2):
            row[seq2_index] = min(
                last_row[seq2_index] + 1,
                row[seq2_index - 1] + 1,
                last_row[seq2_index - 1] + (seq1_char != seq2_char),
            )

    return row[seq2_length - 1]

