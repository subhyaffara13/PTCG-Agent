
def test_program_options(args, result):
    args = args.split()
    assert "example.py" == program.name
    assert result == program.execute(args)

