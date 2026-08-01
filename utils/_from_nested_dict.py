
def _from_nested_dict(
    data: Mapping[HashableT, Mapping[HashableT2, T]],
) -> collections.defaultdict[HashableT2, dict[HashableT, T]]:
    new_data: collections.defaultdict[HashableT2, dict[HashableT, T]] = (
        collections.defaultdict(dict)
    )
    for index, s in data.items():
        for col, v in s.items():
            new_data[col][index] = v
    return new_data

