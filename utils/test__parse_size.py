
def test__parse_size():
    expected = {
        '12': 12e6,
        '12 b': 12,
        '12k': 12e3,
        '  12  M  ': 12e6,
        '  12  G  ': 12e9,
        ' 12Tb ': 12e12,
        '12  Mib ': 12 * 1024.0**2,
        '12Tib': 12 * 1024.0**4,
    }

    for inp, outp in sorted(expected.items()):
        if outp is None:
            with pytest.raises(ValueError):
                _parse_size(inp)
        else:
            assert _parse_size(inp) == outp

