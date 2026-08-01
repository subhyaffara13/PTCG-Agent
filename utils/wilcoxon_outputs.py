
def wilcoxon_outputs(kwds):
    method = kwds.get('method', 'auto')
    if method == 'asymptotic':
        return 3
    return 2

