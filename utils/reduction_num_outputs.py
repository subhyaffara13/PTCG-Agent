
def reduction_num_outputs(reduction_type: str) -> int:
    if is_welford_reduction(reduction_type):
        return 3
    elif reduction_type == "online_softmax_reduce":
        return 2
    else:
        return 1

