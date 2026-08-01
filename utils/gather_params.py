
def gather_params(params, has_biases, has_projections):
    if has_biases and has_projections:
        group_size = 5
    elif has_biases:
        group_size = 4
    elif has_projections:
        group_size = 3
    else:
        group_size = 2

    if len(params) % group_size != 0:
        raise AssertionError(
            f"len(params)={len(params)} is not divisible by group_size={group_size}"
        )
    return [
        tuple(params[i : i + group_size]) for i in range(0, len(params), group_size)
    ]

