
def select_one_layer_lstm_function(input, hx, params):
    r"""Check whether we could use decompose lstm with mkldnn_rnn_layer.
    All the below conditions need to be met:
        * ``torch._C._get_mkldnn_enabled()`` returns ``True``.
        * All the input args are on CPU.
        * The dtypes of args are either torch.float or torch.bfloat16.
        * Inference.
        * ``has_projections`` returns ``False``.

    Args:
        * input: the input sequence to LSTM
        * hx: a tuple of the input hidden state and cell state ``(h_0, c_0)`` to LSTM
        * params: the weight and bias tensors of LSTM
    """

    def use_mkldnn(input, hx, params):
        if not torch._C._get_mkldnn_enabled():
            return False

        tensors = [input] + list(hx) + list(chain.from_iterable(params))
        devices = {t.device for t in tensors}
        if len(devices) != 1:
            return False

        device = devices.pop()
        if device != torch.device("cpu"):
            return False
        # With autocast, possible to have mixed dtype here
        dtypes = {t.dtype for t in tensors}
        for dtype in dtypes:
            if dtype not in [torch.float, torch.bfloat16]:
                return False

        if input.requires_grad:
            return False

        has_projections = hx[0].size(2) != hx[1].size(2)
        if has_projections:
            return False

        return True

    # mkldnn_one_layer_lstm does not depend on seq_len while one_layer_lstm
    # will expand over the seq_len dim
    if use_mkldnn(input, hx, params):
        return mkldnn_one_layer_lstm
    else:
        return one_layer_lstm

