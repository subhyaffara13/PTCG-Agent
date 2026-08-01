
def test_print_SetOp():
    f1 = FiniteSet(x, 1, 3)
    f2 = FiniteSet(y, 2, 4)

    prntr = lambda x: mathml(x, printer='presentation')

    assert prntr(Union(f1, f2, evaluate=False)) == \
    '<mrow><mrow><mo>{</mo><mn>1</mn><mo>,</mo><mn>3</mn><mo>,</mo><mi>x</mi>'\
    '<mo>}</mo></mrow><mo>&#x222A;</mo><mrow><mo>{</mo><mn>2</mn><mo>,</mo>'\
    '<mn>4</mn><mo>,</mo><mi>y</mi><mo>}</mo></mrow></mrow>'
    assert prntr(Intersection(f1, f2, evaluate=False)) == \
    '<mrow><mrow><mo>{</mo><mn>1</mn><mo>,</mo><mn>3</mn><mo>,</mo><mi>x</mi>'\
    '<mo>}</mo></mrow><mo>&#x2229;</mo><mrow><mo>{</mo><mn>2</mn>'\
    '<mo>,</mo><mn>4</mn><mo>,</mo><mi>y</mi><mo>}</mo></mrow></mrow>'
    assert prntr(Complement(f1, f2, evaluate=False)) == \
    '<mrow><mrow><mo>{</mo><mn>1</mn><mo>,</mo><mn>3</mn><mo>,</mo><mi>x</mi>'\
    '<mo>}</mo></mrow><mo>&#x2216;</mo><mrow><mo>{</mo><mn>2</mn>'\
    '<mo>,</mo><mn>4</mn><mo>,</mo><mi>y</mi><mo>}</mo></mrow></mrow>'
    assert prntr(SymmetricDifference(f1, f2, evaluate=False)) == \
    '<mrow><mrow><mo>{</mo><mn>1</mn><mo>,</mo><mn>3</mn><mo>,</mo><mi>x</mi>'\
    '<mo>}</mo></mrow><mo>&#x2206;</mo><mrow><mo>{</mo><mn>2</mn>'\
    '<mo>,</mo><mn>4</mn><mo>,</mo><mi>y</mi><mo>}</mo></mrow></mrow>'

    A = FiniteSet(a)
    C = FiniteSet(c)
    D = FiniteSet(d)

    U1 = Union(C, D, evaluate=False)
    I1 = Intersection(C, D, evaluate=False)
    C1 = Complement(C, D, evaluate=False)
    D1 = SymmetricDifference(C, D, evaluate=False)
    # XXX ProductSet does not support evaluate keyword
    P1 = ProductSet(C, D)

    assert prntr(Union(A, I1, evaluate=False)) == \
        '<mrow><mrow><mo>{</mo><mi>a</mi><mo>}</mo></mrow>' \
        '<mo>&#x222A;</mo><mrow><mo>(</mo><mrow><mrow><mo>{</mo>' \
        '<mi>c</mi><mo>}</mo></mrow><mo>&#x2229;</mo><mrow><mo>{</mo>' \
        '<mi>d</mi><mo>}</mo></mrow></mrow><mo>)</mo></mrow></mrow>'
    assert prntr(Intersection(A, C1, evaluate=False)) == \
        '<mrow><mrow><mo>{</mo><mi>a</mi><mo>}</mo></mrow>' \
        '<mo>&#x2229;</mo><mrow><mo>(</mo><mrow><mrow><mo>{</mo>' \
        '<mi>c</mi><mo>}</mo></mrow><mo>&#x2216;</mo><mrow><mo>{</mo>' \
        '<mi>d</mi><mo>}</mo></mrow></mrow><mo>)</mo></mrow></mrow>'
    assert prntr(Complement(A, D1, evaluate=False)) == \
        '<mrow><mrow><mo>{</mo><mi>a</mi><mo>}</mo></mrow>' \
        '<mo>&#x2216;</mo><mrow><mo>(</mo><mrow><mrow><mo>{</mo>' \
        '<mi>c</mi><mo>}</mo></mrow><mo>&#x2206;</mo><mrow><mo>{</mo>' \
        '<mi>d</mi><mo>}</mo></mrow></mrow><mo>)</mo></mrow></mrow>'
    assert prntr(SymmetricDifference(A, P1, evaluate=False)) == \
        '<mrow><mrow><mo>{</mo><mi>a</mi><mo>}</mo></mrow>' \
        '<mo>&#x2206;</mo><mrow><mo>(</mo><mrow><mrow><mo>{</mo>' \
        '<mi>c</mi><mo>}</mo></mrow><mo>&#x00d7;</mo><mrow><mo>{</mo>' \
        '<mi>d</mi><mo>}</mo></mrow></mrow><mo>)</mo></mrow></mrow>'
    assert prntr(ProductSet(A, U1)) == \
        '<mrow><mrow><mo>{</mo><mi>a</mi><mo>}</mo></mrow>' \
        '<mo>&#x00d7;</mo><mrow><mo>(</mo><mrow><mrow><mo>{</mo>' \
        '<mi>c</mi><mo>}</mo></mrow><mo>&#x222A;</mo><mrow><mo>{</mo>' \
        '<mi>d</mi><mo>}</mo></mrow></mrow><mo>)</mo></mrow></mrow>'

