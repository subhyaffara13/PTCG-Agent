
def test_program_execute(args, result):
    args = args.split()
    assert result == program.execute(args)
    assert program.parse(args)[0].__name__ == program._current_command

