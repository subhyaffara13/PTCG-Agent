
def _setdiag_dense(m, d):
    step = len(d) + 1
    m.flat[::step] = d

