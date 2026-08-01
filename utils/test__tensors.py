
def test_Tensors():
    i, j, k, l = symbols('i j k l', below_fermi=True, cls=Dummy)
    a, b, c, d = symbols('a b c d', above_fermi=True, cls=Dummy)
    p, q, r, s = symbols('p q r s')

    AT = AntiSymmetricTensor
    assert AT('t', (a, b), (i, j)) == -AT('t', (b, a), (i, j))
    assert AT('t', (a, b), (i, j)) == AT('t', (b, a), (j, i))
    assert AT('t', (a, b), (i, j)) == -AT('t', (a, b), (j, i))
    assert AT('t', (a, a), (i, j)) == 0
    assert AT('t', (a, b), (i, i)) == 0
    assert AT('t', (a, b, c), (i, j)) == -AT('t', (b, a, c), (i, j))
    assert AT('t', (a, b, c), (i, j, k)) == AT('t', (b, a, c), (i, k, j))

    tabij = AT('t', (a, b), (i, j))
    assert tabij.has(a)
    assert tabij.has(b)
    assert tabij.has(i)
    assert tabij.has(j)
    assert tabij.subs(b, c) == AT('t', (a, c), (i, j))
    assert (2*tabij).subs(i, c) == 2*AT('t', (a, b), (c, j))
    assert tabij.symbol == Symbol('t')
    assert latex(tabij) == '{t^{ab}_{ij}}'
    assert str(tabij) == 't((_a, _b),(_i, _j))'

    assert AT('t', (a, a), (i, j)).subs(a, b) == AT('t', (b, b), (i, j))
    assert AT('t', (a, i), (a, j)).subs(a, b) == AT('t', (b, i), (b, j))

    a1, a2, a3, a4 = symbols('alpha1:5')
    u_alpha1234 = AntiSymmetricTensor("u", (a1, a2), (a3, a4))

    assert latex(u_alpha1234) == r'{u^{\alpha_{1}\alpha_{2}}_{\alpha_{3}\alpha_{4}}}'
    assert str(u_alpha1234) == 'u((alpha1, alpha2),(alpha3, alpha4))'

