
def _element_wise_sub(a: Sequence[int], b: Sequence[int]) -> list[int]:
    return [i_a - i_b for i_a, i_b in zip(a, b)]

