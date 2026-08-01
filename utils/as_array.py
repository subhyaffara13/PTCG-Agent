
def as_array(request):
    """
    Boolean fixture to support ExtensionDtype _from_sequence method testing.
    """
    return request.param


def as_array(obj):
    """Return object as ARRAY expression (array constant).
    """
    if isinstance(obj, Expr):
        obj = obj,
    return Expr(Op.ARRAY, obj)

