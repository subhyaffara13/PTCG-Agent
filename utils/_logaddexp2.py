
def _logaddexp2(x1, x2, *, evaluate=True):
    return _lb(Add(_exp2(x1, evaluate=evaluate),
                   _exp2(x2, evaluate=evaluate), evaluate=evaluate))

