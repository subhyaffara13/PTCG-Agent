from typing import Union

def test_set_operators_parenthesis():
    a, b, c, d = symbols('a:d')
    A = FiniteSet(a)
    B = FiniteSet(b)
    C = FiniteSet(c)
    D = FiniteSet(d)

    U1 = Union(A, B, evaluate=False)
    U2 = Union(C, D, evaluate=False)
    I1 = Intersection(A, B, evaluate=False)
    I2 = Intersection(C, D, evaluate=False)
    C1 = Complement(A, B, evaluate=False)
    C2 = Complement(C, D, evaluate=False)
    D1 = SymmetricDifference(A, B, evaluate=False)
    D2 = SymmetricDifference(C, D, evaluate=False)
    # XXX ProductSet does not support evaluate keyword
    P1 = ProductSet(A, B)
    P2 = ProductSet(C, D)

    assert latex(Intersection(A, U2, evaluate=False)) == \
        r'\left\{a\right\} \cap ' \
        r'\left(\left\{c\right\} \cup \left\{d\right\}\right)'
    assert latex(Intersection(U1, U2, evaluate=False)) == \
        r'\left(\left\{a\right\} \cup \left\{b\right\}\right) ' \
        r'\cap \left(\left\{c\right\} \cup \left\{d\right\}\right)'
    assert latex(Intersection(C1, C2, evaluate=False)) == \
        r'\left(\left\{a\right\} \setminus ' \
        r'\left\{b\right\}\right) \cap \left(\left\{c\right\} ' \
        r'\setminus \left\{d\right\}\right)'
    assert latex(Intersection(D1, D2, evaluate=False)) == \
        r'\left(\left\{a\right\} \triangle ' \
        r'\left\{b\right\}\right) \cap \left(\left\{c\right\} ' \
        r'\triangle \left\{d\right\}\right)'
    assert latex(Intersection(P1, P2, evaluate=False)) == \
        r'\left(\left\{a\right\} \times \left\{b\right\}\right) ' \
        r'\cap \left(\left\{c\right\} \times ' \
        r'\left\{d\right\}\right)'

    assert latex(Union(A, I2, evaluate=False)) == \
        r'\left\{a\right\} \cup ' \
        r'\left(\left\{c\right\} \cap \left\{d\right\}\right)'
    assert latex(Union(I1, I2, evaluate=False)) == \
        r'\left(\left\{a\right\} \cap \left\{b\right\}\right) ' \
        r'\cup \left(\left\{c\right\} \cap \left\{d\right\}\right)'
    assert latex(Union(C1, C2, evaluate=False)) == \
        r'\left(\left\{a\right\} \setminus ' \
        r'\left\{b\right\}\right) \cup \left(\left\{c\right\} ' \
        r'\setminus \left\{d\right\}\right)'
    assert latex(Union(D1, D2, evaluate=False)) == \
        r'\left(\left\{a\right\} \triangle ' \
        r'\left\{b\right\}\right) \cup \left(\left\{c\right\} ' \
        r'\triangle \left\{d\right\}\right)'
    assert latex(Union(P1, P2, evaluate=False)) == \
        r'\left(\left\{a\right\} \times \left\{b\right\}\right) ' \
        r'\cup \left(\left\{c\right\} \times ' \
        r'\left\{d\right\}\right)'

    assert latex(Complement(A, C2, evaluate=False)) == \
        r'\left\{a\right\} \setminus \left(\left\{c\right\} ' \
        r'\setminus \left\{d\right\}\right)'
    assert latex(Complement(U1, U2, evaluate=False)) == \
        r'\left(\left\{a\right\} \cup \left\{b\right\}\right) ' \
        r'\setminus \left(\left\{c\right\} \cup ' \
        r'\left\{d\right\}\right)'
    assert latex(Complement(I1, I2, evaluate=False)) == \
        r'\left(\left\{a\right\} \cap \left\{b\right\}\right) ' \
        r'\setminus \left(\left\{c\right\} \cap ' \
        r'\left\{d\right\}\right)'
    assert latex(Complement(D1, D2, evaluate=False)) == \
        r'\left(\left\{a\right\} \triangle ' \
        r'\left\{b\right\}\right) \setminus ' \
        r'\left(\left\{c\right\} \triangle \left\{d\right\}\right)'
    assert latex(Complement(P1, P2, evaluate=False)) == \
        r'\left(\left\{a\right\} \times \left\{b\right\}\right) '\
        r'\setminus \left(\left\{c\right\} \times '\
        r'\left\{d\right\}\right)'

    assert latex(SymmetricDifference(A, D2, evaluate=False)) == \
        r'\left\{a\right\} \triangle \left(\left\{c\right\} ' \
        r'\triangle \left\{d\right\}\right)'
    assert latex(SymmetricDifference(U1, U2, evaluate=False)) == \
        r'\left(\left\{a\right\} \cup \left\{b\right\}\right) ' \
        r'\triangle \left(\left\{c\right\} \cup ' \
        r'\left\{d\right\}\right)'
    assert latex(SymmetricDifference(I1, I2, evaluate=False)) == \
        r'\left(\left\{a\right\} \cap \left\{b\right\}\right) ' \
        r'\triangle \left(\left\{c\right\} \cap ' \
        r'\left\{d\right\}\right)'
    assert latex(SymmetricDifference(C1, C2, evaluate=False)) == \
        r'\left(\left\{a\right\} \setminus ' \
        r'\left\{b\right\}\right) \triangle ' \
        r'\left(\left\{c\right\} \setminus \left\{d\right\}\right)'
    assert latex(SymmetricDifference(P1, P2, evaluate=False)) == \
        r'\left(\left\{a\right\} \times \left\{b\right\}\right) ' \
        r'\triangle \left(\left\{c\right\} \times ' \
        r'\left\{d\right\}\right)'

    # XXX This can be incorrect since cartesian product is not associative
    assert latex(ProductSet(A, P2).flatten()) == \
        r'\left\{a\right\} \times \left\{c\right\} \times ' \
        r'\left\{d\right\}'
    assert latex(ProductSet(U1, U2)) == \
        r'\left(\left\{a\right\} \cup \left\{b\right\}\right) ' \
        r'\times \left(\left\{c\right\} \cup ' \
        r'\left\{d\right\}\right)'
    assert latex(ProductSet(I1, I2)) == \
        r'\left(\left\{a\right\} \cap \left\{b\right\}\right) ' \
        r'\times \left(\left\{c\right\} \cap ' \
        r'\left\{d\right\}\right)'
    assert latex(ProductSet(C1, C2)) == \
        r'\left(\left\{a\right\} \setminus ' \
        r'\left\{b\right\}\right) \times \left(\left\{c\right\} ' \
        r'\setminus \left\{d\right\}\right)'
    assert latex(ProductSet(D1, D2)) == \
        r'\left(\left\{a\right\} \triangle ' \
        r'\left\{b\right\}\right) \times \left(\left\{c\right\} ' \
        r'\triangle \left\{d\right\}\right)'

