
def _sub_func(expr, sub_dict):
    """Perform direct matching substitution, ignoring derivatives."""
    if expr in sub_dict:
        return sub_dict[expr]
    elif not expr.args or expr.is_Derivative:
        return expr

