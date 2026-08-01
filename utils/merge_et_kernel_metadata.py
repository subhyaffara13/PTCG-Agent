
def merge_et_kernel_metadata(
    lhs: dict[str, list[str]],
    rhs: dict[str, list[str]],
) -> dict[str, list[str]]:
    merge_et_kernel_metadata: dict[str, set[str]] = defaultdict(set)
    for op in list(lhs.keys()) + list(rhs.keys()):
        merge_et_kernel_metadata[op].update(lhs.get(op, []))
        merge_et_kernel_metadata[op].update(rhs.get(op, []))

    return {op: sorted(val) for op, val in merge_et_kernel_metadata.items()}

