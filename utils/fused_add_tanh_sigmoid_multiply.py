
def fused_add_tanh_sigmoid_multiply(input_a, input_b, num_channels):
    in_act = input_a + input_b
    t_act = torch.tanh(in_act[:, :num_channels, :])
    s_act = torch.sigmoid(in_act[:, num_channels:, :])
    acts = t_act * s_act
    return acts

