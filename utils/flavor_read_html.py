
def flavor_read_html(request):
    return partial(read_html, flavor=request.param)

