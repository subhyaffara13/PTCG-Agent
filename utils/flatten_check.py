
def flatten_check(tensor_type, start_dim, end_dim):
    l = len(tensor_type.__args__)

    start_dim = l if start_dim == -1 else abs(start_dim)
    end_dim = l + end_dim + 1 if end_dim < 0 else end_dim + 1

    if 0 <= start_dim <= (l - 1) and 0 <= end_dim <= l and start_dim < end_dim:
        my_args = list(tensor_type.__args__)
        lhs = my_args[0:start_dim]
        rhs = my_args[end_dim:]
        mid = my_args[start_dim:end_dim]
        if Dyn in mid:
            mid = [Dyn]
        else:
            mid = [reduce(operator.mul, my_args[start_dim:end_dim])]
        new_type_list = lhs + mid + rhs
        return TensorType(tuple(new_type_list))
    else:
        raise TypeError(
            f"Incompatible dimensions {start_dim}, {end_dim - 1} in type {tensor_type}"
        )

