
def run_stubtest_with_stderr(
    stub: str,
    runtime: str,
    options: list[str],
    config_file: str | None = None,
    output: io.StringIO | None = None,
    outerr: io.StringIO | None = None,
) -> tuple[str, str]:
    with use_tmp_dir(TEST_MODULE_NAME) as tmp_dir:
        with open("builtins.pyi", "w") as f:
            f.write(stubtest_builtins_stub)
        with open("typing.pyi", "w") as f:
            f.write(stubtest_typing_stub)
        with open("enum.pyi", "w") as f:
            f.write(stubtest_enum_stub)
        with open(f"{TEST_MODULE_NAME}.pyi", "w") as f:
            f.write(stub)
        with open(f"{TEST_MODULE_NAME}.py", "w") as f:
            f.write(runtime)
        if config_file:
            with open(f"{TEST_MODULE_NAME}_config.ini", "w") as f:
                f.write(config_file)
            options = options + ["--mypy-config-file", f"{TEST_MODULE_NAME}_config.ini"]
        output = io.StringIO() if output is None else output
        outerr = io.StringIO() if outerr is None else outerr
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(outerr):
            test_stubs(parse_options([TEST_MODULE_NAME] + options), use_builtins_fixtures=True)
    filtered_output = remove_color_code(
        output.getvalue()
        # remove cwd as it's not available from outside
        .replace(os.path.realpath(tmp_dir) + os.sep, "").replace(tmp_dir + os.sep, "")
    )
    filtered_outerr = remove_color_code(
        outerr.getvalue()
        # remove cwd as it's not available from outside
        .replace(os.path.realpath(tmp_dir) + os.sep, "").replace(tmp_dir + os.sep, "")
    )
    return filtered_output, filtered_outerr

