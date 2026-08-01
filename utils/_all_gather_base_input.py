
def _all_gather_base_input(input, pg):
    """
    Use _all_gather_base to get a concatenated input from each rank.

    Args:
        input: tensor to be applied op on.
        pg: process group.

    Returns:
        gathered_inputs: input gathered from each rank and concat by dim 0.
    """
    # allgather the inputs first.
    gather_inp_size = list(input.size())
    gather_inp_size[0] = input.size(0) * dist.get_world_size(pg)
    gather_inp = torch.empty(gather_inp_size, device=input.device, dtype=input.dtype)
    return _all_gather_base(gather_inp, input, group=pg)

