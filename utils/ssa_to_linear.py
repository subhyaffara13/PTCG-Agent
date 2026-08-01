
def ssa_to_linear(ssa_path: PathType) -> PathType:
    """Convert a path with static single assignment ids to a path with recycled
    linear ids.

    Example:
        ```python
        ssa_to_linear([(0, 3), (2, 4), (1, 5)])
        #> [(0, 3), (1, 2), (0, 1)]
        ```
    """
    # ids = np.arange(1 + max(map(max, ssa_path)), dtype=np.int32)  # type: ignore
    # path = []
    # for ssa_ids in ssa_path:
    #     path.append(tuple(int(ids[ssa_id]) for ssa_id in ssa_ids))
    #     for ssa_id in ssa_ids:
    #         ids[ssa_id:] -= 1
    # return path

    n = sum(map(len, ssa_path)) - len(ssa_path) + 1
    ids = list(range(n))
    path = []
    ssa = n
    for scon in ssa_path:
        con = sorted([bisect.bisect_left(ids, s) for s in scon])
        for j in reversed(con):
            ids.pop(j)
        ids.append(ssa)
        path.append(con)
        ssa += 1
    return [tuple(x) for x in path]

