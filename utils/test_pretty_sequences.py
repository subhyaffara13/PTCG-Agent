
def test_pretty_sequences():
    s1 = SeqFormula(a**2, (0, oo))
    s2 = SeqPer((1, 2))

    ascii_str = '[0, 1, 4, 9, ...]'
    ucode_str = '[0, 1, 4, 9, …]'

    assert pretty(s1) == ascii_str
    assert upretty(s1) == ucode_str

    ascii_str = '[1, 2, 1, 2, ...]'
    ucode_str = '[1, 2, 1, 2, …]'
    assert pretty(s2) == ascii_str
    assert upretty(s2) == ucode_str

    s3 = SeqFormula(a**2, (0, 2))
    s4 = SeqPer((1, 2), (0, 2))

    ascii_str = '[0, 1, 4]'
    ucode_str = '[0, 1, 4]'

    assert pretty(s3) == ascii_str
    assert upretty(s3) == ucode_str

    ascii_str = '[1, 2, 1]'
    ucode_str = '[1, 2, 1]'
    assert pretty(s4) == ascii_str
    assert upretty(s4) == ucode_str

    s5 = SeqFormula(a**2, (-oo, 0))
    s6 = SeqPer((1, 2), (-oo, 0))

    ascii_str = '[..., 9, 4, 1, 0]'
    ucode_str = '[…, 9, 4, 1, 0]'

    assert pretty(s5) == ascii_str
    assert upretty(s5) == ucode_str

    ascii_str = '[..., 2, 1, 2, 1]'
    ucode_str = '[…, 2, 1, 2, 1]'
    assert pretty(s6) == ascii_str
    assert upretty(s6) == ucode_str

    ascii_str = '[1, 3, 5, 11, ...]'
    ucode_str = '[1, 3, 5, 11, …]'

    assert pretty(SeqAdd(s1, s2)) == ascii_str
    assert upretty(SeqAdd(s1, s2)) == ucode_str

    ascii_str = '[1, 3, 5]'
    ucode_str = '[1, 3, 5]'

    assert pretty(SeqAdd(s3, s4)) == ascii_str
    assert upretty(SeqAdd(s3, s4)) == ucode_str

    ascii_str = '[..., 11, 5, 3, 1]'
    ucode_str = '[…, 11, 5, 3, 1]'

    assert pretty(SeqAdd(s5, s6)) == ascii_str
    assert upretty(SeqAdd(s5, s6)) == ucode_str

    ascii_str = '[0, 2, 4, 18, ...]'
    ucode_str = '[0, 2, 4, 18, …]'

    assert pretty(SeqMul(s1, s2)) == ascii_str
    assert upretty(SeqMul(s1, s2)) == ucode_str

    ascii_str = '[0, 2, 4]'
    ucode_str = '[0, 2, 4]'

    assert pretty(SeqMul(s3, s4)) == ascii_str
    assert upretty(SeqMul(s3, s4)) == ucode_str

    ascii_str = '[..., 18, 4, 2, 0]'
    ucode_str = '[…, 18, 4, 2, 0]'

    assert pretty(SeqMul(s5, s6)) == ascii_str
    assert upretty(SeqMul(s5, s6)) == ucode_str

    # Sequences with symbolic limits, issue 12629
    s7 = SeqFormula(a**2, (a, 0, x))
    raises(NotImplementedError, lambda: pretty(s7))
    raises(NotImplementedError, lambda: upretty(s7))

    b = Symbol('b')
    s8 = SeqFormula(b*a**2, (a, 0, 2))
    ascii_str = '[0, b, 4*b]'
    ucode_str = '[0, b, 4⋅b]'
    assert pretty(s8) == ascii_str
    assert upretty(s8) == ucode_str

