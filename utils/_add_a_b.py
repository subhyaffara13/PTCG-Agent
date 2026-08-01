
def _add_a_b(tests):
    r"""Add "a" and "b" keys to each test from the "bracket" value"""
    for d in tests:
        for k, v in zip(['a', 'b'], d.get('bracket', [])):
            d[k] = v

