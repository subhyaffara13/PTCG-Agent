
def avg_pool3d_backward_shape_check(
    input: Tensor,
    grad_output: Tensor,
    nslices: int,
    kT: int,
    kH: int,
    kW: int,
    dT: int,
    dH: int,
    dW: int,
    pT: int,
    pH: int,
    pW: int,
    itime: int,
    iheight: int,
    iwidth: int,
    otime: int,
    oheight: int,
    owidth: int,
    fn_name: str,
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
        1,
        1,
        1,
        itime,
        iheight,
        iwidth,
        otime,
        oheight,
        owidth,
        fn_name,
        True,
    )

    check_dim_size(grad_output, ndim, ndim - 4, nslices)
    check_dim_size(grad_output, ndim, ndim - 3, otime)
    check_dim_size(grad_output, ndim, ndim - 2, oheight)
    check_dim_size(grad_output, ndim, ndim - 1, owidth)

