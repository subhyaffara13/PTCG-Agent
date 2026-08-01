
def aatype_to_str_sequence(aatype: Sequence[int]) -> str:
    return "".join([restypes_with_x[aatype[i]] for i in range(len(aatype))])

