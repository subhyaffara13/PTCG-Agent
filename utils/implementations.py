
def implementations(request):
    global mminfo
    global mmread
    global mmwrite
    mminfo = request.param.mminfo
    mmread = request.param.mmread
    mmwrite = request.param.mmwrite

