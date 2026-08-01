
def _get_axis_params(default_axis=0, _name=_name, _desc=_desc):  # bind NOW
    _type = f"int or None, default: {default_axis}"
    _axis_parameter_doc = Parameter(_name, _type, _desc)
    _axis_parameter = inspect.Parameter(_name,
                                        inspect.Parameter.KEYWORD_ONLY,
                                        default=default_axis)
    return _axis_parameter_doc, _axis_parameter

