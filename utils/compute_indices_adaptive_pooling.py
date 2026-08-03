import functools

def compute_indices_adaptive_pooling(start_index, end_index, h_in, w_in, h_out, w_out):
    h_start_index = functools.partial(start_index, out_dim=h_out, inp_dim=h_in)
    h_end_index = functools.partial(end_index, out_dim=h_out, inp_dim=h_in)

    w_start_index = functools.partial(start_index, out_dim=w_out, inp_dim=w_in)
    w_end_index = functools.partial(end_index, out_dim=w_out, inp_dim=w_in)

    return h_start_index, h_end_index, w_start_index, w_end_index

