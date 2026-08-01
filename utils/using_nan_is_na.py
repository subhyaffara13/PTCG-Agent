
def using_nan_is_na(request):
    opt = request.param
    with pd.option_context("future.distinguish_nan_and_na", not opt):
        yield opt

