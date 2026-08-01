
def iterparse(*args, **kwargs):
    raise NotSupportedError("defused lxml.etree.iterparse not available")


def iterparse(request):
    return request.param

