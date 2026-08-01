
def pattern_match(request):
    return map(make_local_path, request.param)

