
def test_generic_commands(args, rest):
    args = args.split()
    if len(rest) == 1:
        to_args = rest[0]
        real_name = args[0]
    else:
        to_args = rest[0]
        real_name = rest[1]
    parsed = program.parse(args)
    assert real_name == parsed[0].__name__
    assert to_args == parsed[1]

