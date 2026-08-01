
def pattern_mismatch(request):
    return map(make_local_path, request.param)

