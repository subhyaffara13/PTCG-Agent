
def test_program_except(args, expectation):
    args = args.split()

    with expectation:
        program.execute(args)

        assert program.parse(args)[0].__name__ == program._current_command

