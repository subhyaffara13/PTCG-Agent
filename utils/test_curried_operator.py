
def test_curried_operator():
    import operator

    for k, v in vars(cop).items():
        if not callable(v):
            continue

        if not isinstance(v, toolz.curry):
            try:
                # Make sure it is unary
                v(1)
            except TypeError:
                try:
                    v('x')
                except TypeError:
                    pass
                else:
                    continue
                raise AssertionError(
                    'toolz.curried.operator.%s is not curried!' % k,
                )
        assert should_curry(getattr(operator, k)) == isinstance(v, toolz.curry), k

    # Make sure this isn't totally empty.
    assert len(set(vars(cop)) & {'add', 'sub', 'mul'}) == 3

