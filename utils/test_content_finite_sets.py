from typing import Union

def test_content_finite_sets():
    assert mathml(FiniteSet(a)) == '<set><ci>a</ci></set>'
    assert mathml(FiniteSet(a, b)) == '<set><ci>a</ci><ci>b</ci></set>'
    assert mathml(FiniteSet(FiniteSet(a, b), c)) == \
        '<set><ci>c</ci><set><ci>a</ci><ci>b</ci></set></set>'

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
    # XXX ProductSet does not support evaluate keyword
    P1 = ProductSet(A, B)
    P2 = ProductSet(C, D)

    assert mathml(U1) == \
        '<apply><union/><set><ci>a</ci></set><set><ci>b</ci></set></apply>'
    assert mathml(I1) == \
        '<apply><intersect/><set><ci>a</ci></set><set><ci>b</ci></set>' \
        '</apply>'
    assert mathml(C1) == \
        '<apply><setdiff/><set><ci>a</ci></set><set><ci>b</ci></set></apply>'
    assert mathml(P1) == \
        '<apply><cartesianproduct/><set><ci>a</ci></set><set><ci>b</ci>' \
        '</set></apply>'

    assert mathml(Intersection(A, U2, evaluate=False)) == \
        '<apply><intersect/><set><ci>a</ci></set><apply><union/><set>' \
        '<ci>c</ci></set><set><ci>d</ci></set></apply></apply>'
    assert mathml(Intersection(U1, U2, evaluate=False)) == \
        '<apply><intersect/><apply><union/><set><ci>a</ci></set><set>' \
        '<ci>b</ci></set></apply><apply><union/><set><ci>c</ci></set>' \
        '<set><ci>d</ci></set></apply></apply>'

    # XXX Does the parenthesis appear correctly for these examples in mathjax?
    assert mathml(Intersection(C1, C2, evaluate=False)) == \
        '<apply><intersect/><apply><setdiff/><set><ci>a</ci></set><set>' \
        '<ci>b</ci></set></apply><apply><setdiff/><set><ci>c</ci></set>' \
        '<set><ci>d</ci></set></apply></apply>'
    assert mathml(Intersection(P1, P2, evaluate=False)) == \
        '<apply><intersect/><apply><cartesianproduct/><set><ci>a</ci></set>' \
        '<set><ci>b</ci></set></apply><apply><cartesianproduct/><set>' \
        '<ci>c</ci></set><set><ci>d</ci></set></apply></apply>'

    assert mathml(Union(A, I2, evaluate=False)) == \
        '<apply><union/><set><ci>a</ci></set><apply><intersect/><set>' \
        '<ci>c</ci></set><set><ci>d</ci></set></apply></apply>'
    assert mathml(Union(I1, I2, evaluate=False)) == \
        '<apply><union/><apply><intersect/><set><ci>a</ci></set><set>' \
        '<ci>b</ci></set></apply><apply><intersect/><set><ci>c</ci></set>' \
        '<set><ci>d</ci></set></apply></apply>'
    assert mathml(Union(C1, C2, evaluate=False)) == \
        '<apply><union/><apply><setdiff/><set><ci>a</ci></set><set>' \
        '<ci>b</ci></set></apply><apply><setdiff/><set><ci>c</ci></set>' \
        '<set><ci>d</ci></set></apply></apply>'
    assert mathml(Union(P1, P2, evaluate=False)) == \
        '<apply><union/><apply><cartesianproduct/><set><ci>a</ci></set>' \
        '<set><ci>b</ci></set></apply><apply><cartesianproduct/><set>' \
        '<ci>c</ci></set><set><ci>d</ci></set></apply></apply>'

    assert mathml(Complement(A, C2, evaluate=False)) == \
        '<apply><setdiff/><set><ci>a</ci></set><apply><setdiff/><set>' \
        '<ci>c</ci></set><set><ci>d</ci></set></apply></apply>'
    assert mathml(Complement(U1, U2, evaluate=False)) == \
        '<apply><setdiff/><apply><union/><set><ci>a</ci></set><set>' \
        '<ci>b</ci></set></apply><apply><union/><set><ci>c</ci></set>' \
        '<set><ci>d</ci></set></apply></apply>'
    assert mathml(Complement(I1, I2, evaluate=False)) == \
        '<apply><setdiff/><apply><intersect/><set><ci>a</ci></set><set>' \
        '<ci>b</ci></set></apply><apply><intersect/><set><ci>c</ci></set>' \
        '<set><ci>d</ci></set></apply></apply>'
    assert mathml(Complement(P1, P2, evaluate=False)) == \
        '<apply><setdiff/><apply><cartesianproduct/><set><ci>a</ci></set>' \
        '<set><ci>b</ci></set></apply><apply><cartesianproduct/><set>' \
        '<ci>c</ci></set><set><ci>d</ci></set></apply></apply>'

    assert mathml(ProductSet(A, P2)) == \
        '<apply><cartesianproduct/><set><ci>a</ci></set>' \
        '<apply><cartesianproduct/><set><ci>c</ci></set>' \
        '<set><ci>d</ci></set></apply></apply>'
    assert mathml(ProductSet(U1, U2)) == \
        '<apply><cartesianproduct/><apply><union/><set><ci>a</ci></set>' \
        '<set><ci>b</ci></set></apply><apply><union/><set><ci>c</ci></set>' \
        '<set><ci>d</ci></set></apply></apply>'
    assert mathml(ProductSet(I1, I2)) == \
        '<apply><cartesianproduct/><apply><intersect/><set><ci>a</ci></set>' \
        '<set><ci>b</ci></set></apply><apply><intersect/><set>' \
        '<ci>c</ci></set><set><ci>d</ci></set></apply></apply>'
    assert mathml(ProductSet(C1, C2)) == \
        '<apply><cartesianproduct/><apply><setdiff/><set><ci>a</ci></set>' \
        '<set><ci>b</ci></set></apply><apply><setdiff/><set>' \
        '<ci>c</ci></set><set><ci>d</ci></set></apply></apply>'

