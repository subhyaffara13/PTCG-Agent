
def gen_to_channel_last_perm(rank):
    assert rank > 2, "Shape rank should >2 for the Transpose node."
    perm = []
    perm.append(0)
    for i in range(2, rank):
        perm.append(i)  # noqa: PERF402
    perm.append(1)

    return perm

