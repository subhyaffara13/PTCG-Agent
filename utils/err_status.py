
def err_status():
    err = np.geterr()
    np.seterr(divide='ignore', invalid='ignore')
    yield err
    np.seterr(**err)

