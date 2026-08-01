
def test_pep561(testcase: DataDrivenTestCase) -> None:
    """Test running mypy on files that depend on PEP 561 packages."""
    assert testcase.old_cwd is not None, "test was not properly set up"
    python = sys.executable

    assert python is not None, "Should be impossible"
    pkgs, pip_args = parse_pkgs(testcase.input[0])
    mypy_args = parse_mypy_args(testcase.input[1])
    editable = False
    for arg in pip_args:
        if arg == "editable":
            editable = True
        else:
            raise ValueError(f"Unknown pip argument: {arg}")
    assert pkgs, "No packages to install for PEP 561 test?"
    with virtualenv(python) as venv:
        venv_dir, python_executable = venv
        if editable:
            # Editable installs with PEP 660 require pip>=21.3
            upgrade_pip(python_executable)
        for pkg in pkgs:
            install_package(pkg, python_executable, editable)

        cmd_line = list(mypy_args)
        has_program = not ("-p" in cmd_line or "--package" in cmd_line)
        if has_program:
            program = testcase.name + ".py"
            with open(program, "w", encoding="utf-8") as f:
                for s in testcase.input:
                    f.write(f"{s}\n")
            cmd_line.append(program)

        cmd_line.extend(["--no-error-summary", "--hide-error-codes"])
        if python_executable != sys.executable:
            cmd_line.append(f"--python-executable={python_executable}")

        steps = testcase.find_steps()
        if steps != [[]]:
            steps = [[]] + steps

        for i, operations in enumerate(steps):
            perform_file_operations(operations)

            output = []
            # Type check the module
            out, err, returncode = mypy.api.run(cmd_line)

            # split lines, remove newlines, and remove directory of test case
            for line in (out + err).splitlines():
                if line.startswith(test_temp_dir + os.sep):
                    output.append(line[len(test_temp_dir + os.sep) :].rstrip("\r\n"))
                else:
                    # Normalize paths so that the output is the same on Windows and Linux/macOS.
                    # Yes, this is naive: replace all slashes preceding first colon, if any.
                    path, *rest = line.split(":", maxsplit=1)
                    if rest:
                        path = path.replace(os.sep, "/")
                    output.append(":".join([path, *rest]).rstrip("\r\n"))
            iter_count = "" if i == 0 else f" on iteration {i + 1}"
            expected = testcase.output if i == 0 else testcase.output2.get(i + 1, [])

            assert_string_arrays_equal(
                expected,
                output,
                f"Invalid output ({testcase.file}, line {testcase.line}){iter_count}",
            )

        if has_program:
            os.remove(program)

