import sys

def test_daemon(testcase: DataDrivenTestCase) -> None:
    assert testcase.old_cwd is not None, "test was not properly set up"
    for i, step in enumerate(parse_script(testcase.input)):
        cmd = step[0]
        expected_lines = step[1:]
        assert cmd.startswith("$")
        cmd = cmd[1:].strip()
        cmd = cmd.replace("{python}", sys.executable)
        sts, output = run_cmd(cmd)
        output_lines = output.splitlines()
        output_lines = normalize_error_messages(output_lines)
        if sts:
            output_lines.append("== Return code: %d" % sts)
        assert_string_arrays_equal(
            expected_lines,
            output_lines,
            "Command %d (%s) did not give expected output" % (i + 1, cmd),
        )

