
def _get_truthtable(variables, expr, const):
    """ Return a list of all combinations leading to a True result for ``expr``.
    """
    _variables = variables.copy()
    def _get_tt(inputs):
        if _variables:
            v = _variables.pop()
            tab = [[i[0].xreplace({v: false}), [0] + i[1]] for i in inputs if i[0] is not false]
            tab.extend([[i[0].xreplace({v: true}), [1] + i[1]] for i in inputs if i[0] is not false])
            return _get_tt(tab)
        return inputs
    res = [const + k[1] for k in _get_tt([[expr, []]]) if k[0]]
    if res == [[]]:
        return []
    else:
        return res

