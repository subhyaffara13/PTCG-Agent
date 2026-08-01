
def test_translate():
    abc = 'abc'
    assert translate(abc, None, 'a') == 'bc'
    assert translate(abc, None, '') == 'abc'
    assert translate(abc, {'a': 'x'}, 'c') == 'xb'
    assert translate(abc, {'a': 'bc'}, 'c') == 'bcb'
    assert translate(abc, {'ab': 'x'}, 'c') == 'x'
    assert translate(abc, {'ab': ''}, 'c') == ''
    assert translate(abc, {'bc': 'x'}, 'c') == 'ab'
    assert translate(abc, {'abc': 'x', 'a': 'y'}) == 'x'
    u = chr(4096)
    assert translate(abc, 'a', 'x', u) == 'xbc'
    assert (u in translate(abc, 'a', u, u)) is True


def test_translate():
    s = 'Alpha'
    assert translate(s) == r'\mathrm{A}'
    s = 'Beta'
    assert translate(s) == r'\mathrm{B}'
    s = 'Eta'
    assert translate(s) == r'\mathrm{H}'
    s = 'omicron'
    assert translate(s) == r'o'
    s = 'Pi'
    assert translate(s) == r'\Pi'
    s = 'pi'
    assert translate(s) == r'\pi'
    s = 'LamdaHatDOT'
    assert translate(s) == r'\dot{\hat{\Lambda}}'


def test_translate(index_or_series, any_string_dtype, infer_string):
    obj = index_or_series(
        ["abcdefg", "abcc", "cdddfg", "cdefggg"], dtype=any_string_dtype
    )
    table = str.maketrans("abc", "cde")
    result = obj.str.translate(table)
    expected = index_or_series(
        ["cdedefg", "cdee", "edddfg", "edefggg"], dtype=any_string_dtype
    )
    tm.assert_equal(result, expected)

