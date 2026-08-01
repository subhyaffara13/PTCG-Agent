
def build_kwargs(sep, excel):
    kwargs = {}
    if excel != "default":
        kwargs["excel"] = excel
    if sep != "default":
        kwargs["sep"] = sep
    return kwargs

