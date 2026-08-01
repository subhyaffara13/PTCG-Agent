
def _similar_names(
    owner: SuccessfulInferenceResult,
    attrname: str | None,
    distance_threshold: int,
    max_choices: int,
) -> list[str]:
    """Given an owner and a name, try to find similar names.

    The similar names are searched given a distance metric and only
    a given number of choices will be returned.
    """
    possible_names: list[tuple[str, int]] = []
    names = _node_names(owner)

    attr_str = attrname or ""
    attr_len = len(attr_str)

    for name in names:
        if name == attrname:
            continue

        name_len = len(name)

        min_distance = abs(attr_len - name_len)
        if min_distance > distance_threshold:
            continue

        distance = _string_distance(attr_str, name, attr_len, name_len)
        if distance <= distance_threshold:
            possible_names.append((name, distance))

    # Now get back the values with a minimum, up to the given
    # limit or choices.
    picked = [
        name
        for (name, _) in heapq.nsmallest(
            max_choices, possible_names, key=operator.itemgetter(1)
        )
    ]
    return sorted(picked)

