
def _eval_length(length, params):
    if length in ['(:)', '(*)', '*']:
        return '(*)'
    return _eval_scalar(length, params)

