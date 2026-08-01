
def test_printing():
    for c in (LatexPrinter, LatexPrinter(), MathMLContentPrinter,
              MathMLPresentationPrinter, PrettyPrinter, prettyForm, stringPict,
              stringPict("a"), Printer, Printer(), PythonPrinter,
              PythonPrinter()):
        check(c)


def test_printing():
    R = QQ.old_poly_ring(x)

    assert str(homomorphism(R.free_module(1), R.free_module(1), [0])) == \
        'Matrix([[0]]) : QQ[x]**1 -> QQ[x]**1'
    assert str(homomorphism(R.free_module(2), R.free_module(2), [0, 0])) == \
        'Matrix([                       \n[0, 0], : QQ[x]**2 -> QQ[x]**2\n[0, 0]])                       '
    assert str(homomorphism(R.free_module(1), R.free_module(1) / [[x]], [0])) == \
        'Matrix([[0]]) : QQ[x]**1 -> QQ[x]**1/<[x]>'
    assert str(R.free_module(0).identity_hom()) == 'Matrix(0, 0, []) : QQ[x]**0 -> QQ[x]**0'


def test_printing():
    assert latex(sx) == r'{\sigma_x}'
    assert latex(sx1) == r'{\sigma_x^{(1)}}'
    assert latex(sy) == r'{\sigma_y}'
    assert latex(sy1) == r'{\sigma_y^{(1)}}'
    assert latex(sz) == r'{\sigma_z}'
    assert latex(sz1) == r'{\sigma_z^{(1)}}'
    assert latex(sm) == r'{\sigma_-}'
    assert latex(sm1) == r'{\sigma_-^{(1)}}'
    assert latex(sp) == r'{\sigma_+}'
    assert latex(sp1) == r'{\sigma_+^{(1)}}'


def test_printing():
    string = "bbd,bda,fc,db->acf"
    views = build_views(string)

    ein = contract_path(string, *views)
    assert len(str(ein[1])) == 728

