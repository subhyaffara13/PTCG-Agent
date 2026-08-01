
def test_generic_command(args, result):
    args = args.split()
    assert result == program.execute(args)
    assert program.parse(args)[0].__name__ == program._current_command


def test_generic_command(args, result):
    args = args.split()
    assert result == program.execute(args)
    assert program.parse(args)[0].__name__ == program._current_command

