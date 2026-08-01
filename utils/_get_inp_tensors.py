
def _get_inp_tensors(tupled_inputs):
    inp_idx_tup = [
        (i, t)
        for i, t in enumerate(tupled_inputs)
        if is_tensor_like(t) and t.requires_grad
    ]
    return [tup[0] for tup in inp_idx_tup], [tup[1] for tup in inp_idx_tup]

