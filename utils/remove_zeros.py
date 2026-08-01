
def remove_zeros(split_sections: list[int]):
    """
    Remove zeros from the list and get the index mapping dict from getitem
    in split node to getitem in new split node
    """
    new_split_sections, index_mapping = [], {}
    idx = 0
    for i in range(len(split_sections)):
        if split_sections[i] > 0:
            new_split_sections.append(split_sections[i])
            index_mapping[i] = idx
            idx += 1

    return new_split_sections, index_mapping

