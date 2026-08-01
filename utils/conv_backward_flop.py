
def conv_backward_flop(
        grad_out_shape,
        x_shape,
        w_shape,
        _bias,
        _stride,
        _padding,
        _dilation,
        transposed,
        _output_padding,
        _groups,
        output_mask,
        out_shape) -> int:

    def t(shape):
        return [shape[1], shape[0]] + list(shape[2:])
    flop_count = 0

    """
    Let's say we have a regular 1D conv
    {A, B, C} [inp]
    {i, j} [weight]
    => (conv)
    {Ai + Bj, Bi + Cj} [out]

    And as a reminder, the transposed conv of the above is
    => {Ai, Aj + Bi, Bj + Ci, Cj} [transposed conv out]

    For the backwards of conv, we now have
    {D, E} [grad_out]
    {A, B, C} [inp]
    {i, j} [weight]

    # grad_inp as conv_transpose(grad_out, weight)
    Let's first compute grad_inp. To do so, we can simply look at all the
    multiplications that each element of inp is involved in. For example, A is
    only involved in the first element of the output (and thus only depends upon
    D in grad_out), and C is only involved in the last element of the output
    (and thus only depends upon E in grad_out)

    {Di, Dj + Ei, Ej} [grad_inp]

    Note that this corresponds to the below conv_transpose. This gives us the
    output_mask[0] branch, which is grad_inp.

    {D, E} [inp (grad_out)]
    {i, j} [weight]
    => (conv_transpose)
    {Di, Dj + Ei, Ej} [out (grad_inp)]

    I leave the fact that grad_inp for a transposed conv is just conv(grad_out,
    weight) as an exercise for the reader.

    # grad_weight as conv(inp, grad_out)
    To compute grad_weight, we again look at the terms in the output, which as
    a reminder is:
    => {Ai + Bj, Bi + Cj} [out]
    => {D, E} [grad_out]
    If we manually compute the gradient for the weights, we see it's
    {AD + BE, BD + CE} [grad_weight]

    This corresponds to the below conv
    {A, B, C} [inp]
    {D, E} [weight (grad_out)]
    => (conv)
    {AD + BE, BD + CE} [out (grad_weight)]

    # grad_weight of transposed conv as conv(grad_out, inp)
    As a reminder, the terms of the output of a transposed conv are:
    => {Ai, Aj + Bi, Bj + Ci, Cj} [transposed conv out]
    => {D, E, F, G} [grad_out]

    Manually computing the gradient for the weights, we see it's
    {AD + BE + CF, AE + BF + CG} [grad_weight]

    This corresponds to the below conv
    {D, E, F, G} [inp (grad_out)]
    {A, B, C} [weight (inp)]
    => (conv)
    {AD + BE + CF, AE + BF + CG} [out (grad_weight)]

    For the full backwards formula, there are also some details involving
    transpose of the batch/channel dimensions and groups, but I skip those for
    the sake of brevity (and they're pretty similar to matmul backwards)

    Check [conv backwards decomposition as conv forwards]
    """
    # grad_inp as conv_transpose(grad_out, weight)
    if output_mask[0]:
        grad_input_shape = get_shape(out_shape[0])
        flop_count += conv_flop_count(grad_out_shape, w_shape, grad_input_shape, not transposed)

    if output_mask[1]:
        grad_weight_shape = get_shape(out_shape[1])
        if transposed:
            # grad_weight of transposed conv as conv(grad_out, inp)
            flop_count += conv_flop_count(t(grad_out_shape), t(x_shape), t(grad_weight_shape), transposed=False)
        else:
            # grad_weight as conv(inp, grad_out)
            flop_count += conv_flop_count(t(x_shape), t(grad_out_shape), t(grad_weight_shape), transposed=False)

    return flop_count

