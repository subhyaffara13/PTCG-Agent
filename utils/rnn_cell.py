
def rnn_cell(nonlinearity):
    def inner(i, cur_hidden, ih_weight, ih_bias, hh_weight, hh_bias):
        return nonlinearity(F.linear(cur_hidden, hh_weight, hh_bias) + i)

    return inner

