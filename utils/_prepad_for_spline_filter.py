
def _prepad_for_spline_filter(input, mode, cval):
    if mode in ['nearest', 'grid-constant']:
        npad = 12
        if mode == 'grid-constant':
            padded = np.pad(input, npad, mode='constant',
                               constant_values=cval)
        elif mode == 'nearest':
            padded = np.pad(input, npad, mode='edge')
    else:
        # other modes have exact boundary conditions implemented so
        # no prepadding is needed
        npad = 0
        padded = input
    return padded, npad

