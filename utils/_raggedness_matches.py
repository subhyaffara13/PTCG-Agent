
def _raggedness_matches(nt1, nt2):
    return (
        nt1.is_nested
        and nt2.is_nested
        and nt1._ragged_idx == nt2._ragged_idx
        and nt1.shape[nt1._ragged_idx] == nt2.shape[nt2._ragged_idx]
    )

