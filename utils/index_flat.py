
def index_flat(request):
    """
    index fixture, but excluding MultiIndex cases.
    """
    key = request.param
    return indices_dict[key].copy(deep=False)

