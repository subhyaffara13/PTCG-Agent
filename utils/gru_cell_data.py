
def gru_cell_data(inp, cur_hidden, ih_weight, ih_bias, hh_weight, hh_bias):
    chunked_igates = F.linear(inp, ih_weight, ih_bias).chunk(3, 1)
    chunked_hgates = F.linear(cur_hidden, hh_weight, hh_bias).chunk(3, 1)
    reset_gate = (chunked_hgates[0] + chunked_igates[0]).sigmoid()
    input_gate = (chunked_hgates[1] + chunked_igates[1]).sigmoid()
    new_gate = (chunked_igates[2] + (chunked_hgates[2] * reset_gate)).tanh()
    return (cur_hidden - new_gate) * input_gate + new_gate

