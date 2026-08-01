
def mdata_xy(request, reference_data):
    y = reference_data['Y'][request.param]
    x = reference_data['X'][request.param]
    return x, y

