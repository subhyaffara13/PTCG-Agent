
def gen_to_channel_first_perm(rank):
    assert rank > 2, "Shape rank should >2 for the Transpose node."
    perm = []
    perm.append(0)
    perm.append(rank - 1)
    for i in range(1, rank - 1):
        perm.append(i)  # noqa: PERF402

    return perm

