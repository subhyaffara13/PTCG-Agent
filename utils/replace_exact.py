
def replace_exact(d, to_replace, exact):
    for name in to_replace:
        assert name in exact, f'Missing exact value: {name}'
        assert abs(exact[name]/d[name][0] - 1) <= 1e-9, \
            f'Bad exact value: {name}: { exact[name]}, {d[name][0]}'
        d[name] = (exact[name],) + d[name][1:]
    assert set(exact.keys()) == set(to_replace)

