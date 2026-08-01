
def Asp(request):
    A = request.param((3, 3))
    A[(0, 1)] = 1
    A[(0, 2)] = 2
    yield A

