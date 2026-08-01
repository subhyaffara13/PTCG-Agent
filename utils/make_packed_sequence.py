
def make_packed_sequence(inp, batch_sizes):
    required_grad = inp.requires_grad
    inp.requires_grad_(False)  # user won't have access to inp so won't be able to get its grads
    seq = pack_padded_sequence(inp, batch_sizes)
    seq.data.requires_grad_(required_grad)
    return seq

