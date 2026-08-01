
def _compare_approx(
    full_object: object,
    message_data: Sequence[tuple[str, str, str]],
    number_of_elements: int,
    different_ids: Sequence[object],
    max_abs_diff: float,
    max_rel_diff: float,
) -> list[str]:
    message_list = list(message_data)
    message_list.insert(0, ("Index", "Obtained", "Expected"))
    max_sizes = [0, 0, 0]
    for index, obtained, expected in message_list:
        max_sizes[0] = max(max_sizes[0], len(index))
        max_sizes[1] = max(max_sizes[1], len(obtained))
        max_sizes[2] = max(max_sizes[2], len(expected))
    explanation = [
        f"comparison failed. Mismatched elements: {len(different_ids)} / {number_of_elements}:",
        f"Max absolute difference: {max_abs_diff}",
        f"Max relative difference: {max_rel_diff}",
    ] + [
        f"{indexes:<{max_sizes[0]}} | {obtained:<{max_sizes[1]}} | {expected:<{max_sizes[2]}}"
        for indexes, obtained, expected in message_list
    ]
    return explanation

