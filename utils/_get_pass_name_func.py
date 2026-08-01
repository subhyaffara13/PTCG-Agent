
def _get_pass_name_func(p):
    if isinstance(p, PatternMatcherPassBase):
        pass_name = p.pass_name
        pass_func = p.apply
    elif isinstance(p, types.FunctionType):
        pass_name = p.__name__.lstrip("_")
        pass_func = p
    else:
        pass_name = None
        pass_func = None

    return pass_name, pass_func

