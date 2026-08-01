
def get_type_a_related_to_b(
    base_name_to_sets_of_related_ops: dict[str, set[NSNodeTargetType]],
) -> set[tuple[NSNodeTargetType, NSNodeTargetType]]:
    # TODO(future PR): allow customizations
    # TODO(future PR): reuse existing quantization mappings
    # TODO(future PR): add the rest of modules and ops here
    type_a_related_to_b: set[tuple[NSNodeTargetType, NSNodeTargetType]] = set()

    for s in base_name_to_sets_of_related_ops.values():
        s_list = list(s)
        # add every bidirectional pair
        for idx_0 in range(len(s_list)):
            for idx_1 in range(idx_0, len(s_list)):
                type_a_related_to_b.add((s_list[idx_0], s_list[idx_1]))
                type_a_related_to_b.add((s_list[idx_1], s_list[idx_0]))

    return type_a_related_to_b

