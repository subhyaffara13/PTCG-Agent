
def params_hiddens(params, hiddens, i, bidirectional):
    if bidirectional:
        cur_params, cur_hidden = params[2 * i], hiddens[2 * i]
        bidir_params, bidir_hidden = params[2 * i + 1], hiddens[2 * i + 1]
    else:
        cur_params, cur_hidden = params[i], hiddens[i]
        bidir_params, bidir_hidden = None, None

    return cur_params, cur_hidden, bidir_params, bidir_hidden

