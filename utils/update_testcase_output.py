
def update_testcase_output(testcase: DataDrivenTestCase, output: list[str]) -> None:
    # TODO: backport this to mypy
    assert testcase.old_cwd is not None, "test was not properly set up"
    testcase_path = os.path.join(testcase.old_cwd, testcase.file)
    with open(testcase_path) as f:
        data_lines = f.read().splitlines()

    # We can't rely on the test line numbers to *find* the test, since
    # we might fix multiple tests in a run. So find it by the case
    # header. Give up if there are multiple tests with the same name.
    test_slug = f"[case {testcase.name}]"
    if data_lines.count(test_slug) != 1:
        return
    start_idx = data_lines.index(test_slug)
    stop_idx = start_idx + 11
    while stop_idx < len(data_lines) and not data_lines[stop_idx].startswith("[case "):
        stop_idx += 1

    test = data_lines[start_idx:stop_idx]
    out_start = test.index("[out]")
    test[out_start + 1 :] = output
    data_lines[start_idx:stop_idx] = test + [""]
    data = "\n".join(data_lines)

    with open(testcase_path, "w") as f:
        print(data, file=f)


def update_testcase_output(
    testcase: DataDrivenTestCase, actual: list[str], *, incremental_step: int
) -> None:
    if testcase.xfail:
        return
    collector = testcase.parent
    assert isinstance(collector, DataFileCollector)
    for fix in _iter_fixes(testcase, actual, incremental_step=incremental_step):
        collector.enqueue_fix(fix)

