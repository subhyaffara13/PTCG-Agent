
def maxpool2d_check(typ, module_instance):
    """
    Applies the maxpool2d shape information to the input
    this affects the last two dimensions
    """
    new_type_list = list(typ.__args__)
    if len(new_type_list) == 4 or len(new_type_list) == 3:
        w_in = new_type_list[-1]
        h_in = new_type_list[-2]

        h_out = calculate_out_dimension(h_in, module_instance, 0)
        w_out = calculate_out_dimension(w_in, module_instance, 1)

        new_type_list[-1] = w_out
        new_type_list[-2] = h_out
        return TensorType(tuple(new_type_list))

    else:
        raise TypeError(f"Wrong size {typ} for {module_instance}")

