
def _make_all_gather_out_tensor(input, group_size):
    out_size = list(input.size())
    if len(out_size) == 0:
        out_size.append(group_size)
    else:
        out_size[0] *= group_size
    out_tensor = input.new_empty(out_size)
    return out_tensor

