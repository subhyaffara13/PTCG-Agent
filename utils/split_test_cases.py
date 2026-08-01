
def split_test_cases(
    parent: DataFileCollector, suite: DataSuite, file: str
) -> Iterator[DataDrivenTestCase]:
    """Iterate over raw test cases in file, at collection time, ignoring sub items.

    The collection phase is slow, so any heavy processing should be deferred to after
    uninteresting tests are filtered (when using -k PATTERN switch).
    """
    with open(file, encoding="utf-8") as f:
        data = f.read()
    cases = re.split(r"^\[case ([^]+)]+)\][ \t]*$\n", data, flags=re.DOTALL | re.MULTILINE)
    cases_iter = iter(cases)
    line_no = next(cases_iter).count("\n") + 1
    test_names = set()
    for case_id in cases_iter:
        data = next(cases_iter)

        m = _case_name_pattern.fullmatch(case_id)
        if not m:
            raise RuntimeError(f"Invalid testcase id {case_id!r}")
        name = m.group("name")
        if name in test_names:
            raise RuntimeError(
                'Found a duplicate test name "{}" in {} on line {}'.format(
                    name, parent.name, line_no
                )
            )
        yield DataDrivenTestCase.from_parent(
            parent=parent,
            suite=suite,
            file=file,
            name=add_test_name_suffix(name, suite.test_name_suffix),
            writescache=bool(m.group("writescache")),
            only_when=m.group("only_when"),
            platform=m.group("platform"),
            skip=bool(m.group("skip")),
            xfail=bool(m.group("xfail")),
            normalize_output=not m.group("skip_path_normalization"),
            data=data,
            line=line_no,
        )
        line_no += data.count("\n") + 1

        # Record existing tests to prevent duplicates:
        test_names.update({name})

