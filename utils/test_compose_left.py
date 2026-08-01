
def test_compose_left():
    for (compose_left_args, args, kw, expected) in generate_compose_left_test_cases():
        assert compose_left(*compose_left_args)(*args, **kw) == expected

