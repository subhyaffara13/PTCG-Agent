
def _eval_scalar(value, params):
    if _is_kind_number(value):
        value = value.split('_')[0]
    try:
        # TODO: use symbolic from PR #19805
        value = eval(value, {}, params)
        value = (repr if isinstance(value, str) else str)(value)
    except (NameError, SyntaxError, TypeError):
        return value
    except Exception as msg:
        errmess(f'"{msg}" in evaluating {value!r} '
                f'(available names: {list(params)})\n')
    return value

