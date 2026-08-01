
def max_pool3d_backward_shape_check(
    input,
    grad_output,
    indices,
    nslices,
    kT,
    kH,
    kW,
    dT,
    dH,
    dW,
    pT,
    pH,
    pW,
    dilationT,
    dilationH,
    dilationW,
    itime,
    iheight,
    iwidth,
    otime,
    oheight,
    owidth,
    fn_name,
):
    ndim = input.ndim

    pool3d_shape_check(
        input,
        nslices,
        kT,
        kH,
        kW,
        dT,
        dH,
        dW,
        pT,
        pH,
        pW,
        dilationT,
        dilationH,
        dilationW,
        itime,
        iheight,
        iwidth,
        otime,
        oheight,
        owidth,
        fn_name,
    )

    check_dim_size(grad_output, ndim, ndim - 4, nslices)
    check_dim_size(grad_output, ndim, ndim - 3, otime)
    check_dim_size(grad_output, ndim, ndim - 2, oheight)
    check_dim_size(grad_output, ndim, ndim - 1, owidth)

    check_dim_size(indices, ndim, ndim - 4, nslices)
    check_dim_size(indices, ndim, ndim - 3, otime)
    check_dim_size(indices, ndim, ndim - 2, oheight)
    check_dim_size(indices, ndim, ndim - 1, owidth)

