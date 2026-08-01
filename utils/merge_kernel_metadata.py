
def merge_kernel_metadata(
    lhs: dict[str, list[str]],
    rhs: dict[str, list[str]],
) -> dict[str, list[str]]:
    kernel_metadata: dict[str, list[str]] = {}
    for tag_name, dtypes in list(lhs.items()) + list(rhs.items()):
        dtypes_copy = set(dtypes)
        if tag_name in kernel_metadata:
            dtypes_copy |= set(kernel_metadata[tag_name])

        kernel_metadata[tag_name] = list(dtypes_copy)

    return kernel_metadata

