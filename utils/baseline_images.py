
def baseline_images(request, fontset, index, text):
    if text is None:
        pytest.skip("test has been removed")
    return ['%s_%s_%02d' % (request.param, fontset, index)]

