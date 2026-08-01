
def mkldnn_one_layer_lstm(inp, hidden, params, has_biases, reverse=False):
    w0 = params[0]
    w1 = params[1]
    if has_biases:
        w2 = params[2]
        w3 = params[3]
    else:
        w2 = torch.zeros(w0.size())
        w3 = torch.zeros(w1.size())

    hx = hidden[0].unsqueeze(0)
    cx = hidden[1].unsqueeze(0)

    batch_sizes: list[int] = []
    mode = 2  # third_party/ideep/include/ideep/abstract_types.hpp: ideep::rnn_kind::LSTM = 2
    hidden_size = hx.size(2)
    num_layers = 1

    # _rnn_helper already handles bidirectional and batch_first so we hard-code them to False here
    bidirectional = False
    batch_first = False

    train = False
    # If batch_first, inp has been permuted in _rnn_helper. Convert to contiguous here.
    # Same as aten/src/ATen/native/mkldnn/RNN.cpp: mkldnn_rnn: input = input.contiguous();
    inp = inp.contiguous()
    hx = hx.contiguous()
    cx = cx.contiguous()
    outputs = torch.ops.aten.mkldnn_rnn_layer.default(
        inp,
        w0,
        w1,
        w2,
        w3,
        hx,
        cx,
        reverse,
        batch_sizes,
        mode,
        hidden_size,
        num_layers,
        has_biases,
        bidirectional,
        batch_first,
        train,
    )
    y, hy, cy = outputs[0], outputs[1], outputs[2]
    return y, (hy.squeeze(0), cy.squeeze(0))

