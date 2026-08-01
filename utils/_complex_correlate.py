
def _complex_correlate(xp, array, kernel, real_dtype, convolve=False,
                       mode="reflect", cval=0, ):
    """Utility to perform a reference complex-valued convolutions.

    When convolve==False, correlation is performed instead
    """
    array = xp.asarray(array)
    kernel = xp.asarray(kernel)
    complex_array = xp.isdtype(array.dtype, 'complex floating')
    complex_kernel = xp.isdtype(kernel.dtype, 'complex floating')
    if array.ndim == 1:
        func = ndimage.convolve1d if convolve else ndimage.correlate1d
    else:
        func = ndimage.convolve if convolve else ndimage.correlate
    if not convolve:
        kernel = xp.conj(kernel)
    if complex_array and complex_kernel:
        # use: real(cval) for array.real component
        #      imag(cval) for array.imag component
        re_cval = cval.real if isinstance(cval, complex) else xp.real(cval)
        im_cval = cval.imag if isinstance(cval, complex) else xp.imag(cval)

        output = (
            func(xp.real(array), xp.real(kernel), output=real_dtype,
                 mode=mode, cval=re_cval) -
            func(xp.imag(array), xp.imag(kernel), output=real_dtype,
                 mode=mode, cval=im_cval) +
            1j * func(xp.imag(array), xp.real(kernel), output=real_dtype,
                      mode=mode, cval=im_cval) +
            1j * func(xp.real(array), xp.imag(kernel), output=real_dtype,
                      mode=mode, cval=re_cval)
        )
    elif complex_array:
        re_cval = xp.real(cval)
        re_cval = re_cval.item() if isinstance(re_cval, xp.ndarray) else re_cval
        im_cval = xp.imag(cval)
        im_cval = im_cval.item() if isinstance(im_cval, xp.ndarray) else im_cval

        output = (
            func(xp.real(array), kernel, output=real_dtype, mode=mode,
                 cval=re_cval) +
            1j * func(xp.imag(array), kernel, output=real_dtype, mode=mode,
                      cval=im_cval)
        )
    elif complex_kernel:
        # real array so cval is real too
        output = (
            func(array, xp.real(kernel), output=real_dtype, mode=mode, cval=cval) +
            1j * func(array, xp.imag(kernel), output=real_dtype, mode=mode,
                      cval=cval)
        )
    return output

