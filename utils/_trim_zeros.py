
def _trim_zeros(filt, trim='fb'):
    first = 0
    trim = trim.upper()
    if 'F' in trim:
        for i in filt:
            if i != 0.:
                break
            else:
                first = first + 1
    last = filt.shape[0]
    if 'B' in trim:
        for i in filt[::-1]:
            if i != 0.:
                break
            else:
                last = last - 1
    return filt[first:last]


def _trim_zeros(filt, trim=None, axis=None):
    return (filt,)

