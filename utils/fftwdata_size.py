
def fftwdata_size(request, reference_data):
    return reference_data['FFTWDATA_SIZES'][request.param]

