
def test_latex_indexed():
    Psi_symbol = Symbol('Psi_0', complex=True, real=False)
    Psi_indexed = IndexedBase(Symbol('Psi', complex=True, real=False))
    symbol_latex = latex(Psi_symbol * conjugate(Psi_symbol))
    indexed_latex = latex(Psi_indexed[0] * conjugate(Psi_indexed[0]))
    # \\overline{{\\Psi}_{0}} {\\Psi}_{0}  vs.  \\Psi_{0} \\overline{\\Psi_{0}}
    assert symbol_latex == r'\Psi_{0} \overline{\Psi_{0}}'
    assert indexed_latex == r'\overline{{\Psi}_{0}} {\Psi}_{0}'

    # Symbol('gamma') gives r'\gamma'
    interval = '\\mathrel{..}\\nobreak '
    assert latex(Indexed('x1', Symbol('i'))) == r'{x_{1}}_{i}'
    assert latex(Indexed('x2', Idx('i'))) == r'{x_{2}}_{i}'
    assert latex(Indexed('x3', Idx('i', Symbol('N')))) == r'{x_{3}}_{{i}_{0'+interval+'N - 1}}'
    assert latex(Indexed('x3', Idx('i', Symbol('N')+1))) == r'{x_{3}}_{{i}_{0'+interval+'N}}'
    assert latex(Indexed('x4', Idx('i', (Symbol('a'),Symbol('b'))))) == r'{x_{4}}_{{i}_{a'+interval+'b}}'
    assert latex(IndexedBase('gamma')) == r'\gamma'
    assert latex(IndexedBase('a b')) == r'a b'
    assert latex(IndexedBase('a_b')) == r'a_{b}'

