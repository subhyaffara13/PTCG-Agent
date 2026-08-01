
def generate_apply_looper(func, nopython=True, nogil=True, parallel=False):
    if TYPE_CHECKING:
        import numba
    else:
        numba = import_optional_dependency("numba")
    nb_compat_func = jit_user_function(func)

    @numba.jit(nopython=nopython, nogil=nogil, parallel=parallel)
    def nb_looper(values, axis, *args):
        # Operate on the first row/col in order to get
        # the output shape
        if axis == 0:
            first_elem = values[:, 0]
            dim0 = values.shape[1]
        else:
            first_elem = values[0]
            dim0 = values.shape[0]
        res0 = nb_compat_func(first_elem, *args)
        # Use np.asarray to get shape for
        # https://github.com/numba/numba/issues/4202#issuecomment-1185981507
        # Use tuple concatenation; numba doesn't support tuple unpacking syntax
        buf_shape = (dim0,) + np.atleast_1d(np.asarray(res0)).shape  # noqa: RUF005
        if axis == 0:
            buf_shape = buf_shape[::-1]
        buff = np.empty(buf_shape)

        if axis == 1:
            buff[0] = res0
            for i in numba.prange(1, values.shape[0]):
                buff[i] = nb_compat_func(values[i], *args)
        else:
            buff[:, 0] = res0
            for j in numba.prange(1, values.shape[1]):
                buff[:, j] = nb_compat_func(values[:, j], *args)
        return buff

    return nb_looper

