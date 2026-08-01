
def _array_tofile(fid, data):
    # ravel gives a c-contiguous buffer
    fid.write(data.ravel().view('b').data)

