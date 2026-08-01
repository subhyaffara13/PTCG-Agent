
def test_SciPyPrinter():
    p = SciPyPrinter()
    expr = acos(x)
    assert 'numpy' not in p.module_imports
    assert p.doprint(expr) == 'numpy.arccos(x)'
    assert 'numpy' in p.module_imports
    assert not any(m.startswith('scipy') for m in p.module_imports)
    smat = SparseMatrix(2, 5, {(0, 1): 3})
    assert p.doprint(smat) == \
        'scipy.sparse.coo_matrix(([3], ([0], [1])), shape=(2, 5))'
    assert 'scipy.sparse' in p.module_imports

    assert p.doprint(S.GoldenRatio) == 'scipy.constants.golden_ratio'
    assert p.doprint(S.Pi) == 'scipy.constants.pi'
    assert p.doprint(S.Exp1) == 'numpy.e'

