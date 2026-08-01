
def test_tokenize():
    data = (b'1234/abc false -9.81  Foo <<[0 1 2]<0 1ef a\t>>>\n'
            b'(string with(nested\t\\) par)ens\\\\)')
    #         1           2          x    2     xx1
    # 1 and 2 are matching parens, x means escaped character
    n, w, num, kw, d = 'name', 'whitespace', 'number', 'keyword', 'delimiter'
    b, s = 'boolean', 'string'
    correct = [
        (num, 1234), (n, 'abc'), (w, ' '), (b, False), (w, ' '), (num, -9.81),
        (w, '  '), (kw, 'Foo'), (w, ' '), (d, '<<'), (d, '['), (num, 0),
        (w, ' '), (num, 1), (w, ' '), (num, 2), (d, ']'), (s, b'\x01\xef\xa0'),
        (d, '>>'), (w, '\n'), (s, 'string with(nested\t) par)ens\\')
    ]
    correct_no_ws = [x for x in correct if x[0] != w]

    def convert(tokens):
        return [(t.kind, t.value()) for t in tokens]

    assert convert(t1f._tokenize(data, False)) == correct
    assert convert(t1f._tokenize(data, True)) == correct_no_ws

    def bin_after(n):
        tokens = t1f._tokenize(data, True)
        result = []
        for _ in range(n):
            result.append(next(tokens))
        result.append(tokens.send(10))
        return convert(result)

    for n in range(1, len(correct_no_ws)):
        result = bin_after(n)
        assert result[:-1] == correct_no_ws[:n]
        assert result[-1][0] == 'binary'
        assert isinstance(result[-1][1], bytes)

