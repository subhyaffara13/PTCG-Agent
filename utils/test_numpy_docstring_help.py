
def test_numpy_docstring_help(args, result):
    args = args.split()
    with pytest.raises(SystemExit):
        with capture.capture_sys_output() as (stdout, stderr):
            program.execute(args)
    assert result == stdout.getvalue()

