import os
import re
import sys

def parse_test_case(case: DataDrivenTestCase) -> None:
    """Parse and prepare a single case from suite with test case descriptions.

    This method is part of the setup phase, just before the test case is run.
    """
    test_items = parse_test_data(case.data, case.name)
    base_path = case.suite.base_path
    if case.suite.native_sep:
        join = os.path.join
    else:
        join = posixpath.join

    out_section_missing = case.suite.required_out_section

    files: list[tuple[str, str]] = []  # path and contents
    output_files: list[tuple[str, str | Pattern[str]]] = []  # output path and contents
    output: list[str] = []  # Regular output errors
    output2: dict[int, list[str]] = {}  # Output errors for incremental, runs 2+
    deleted_paths: dict[int, set[str]] = {}  # from run number of paths
    stale_modules: dict[int, set[str]] = {}  # from run number to module names
    rechecked_modules: dict[int, set[str]] = {}  # from run number module names
    triggered: list[str] = []  # Active triggers (one line per incremental step)
    targets: dict[int, list[str]] = {}  # Fine-grained targets (per fine-grained update)
    test_modules: list[str] = []  # Modules which are deemed "test" (vs "fixture")

    def _case_fail(msg: str) -> NoReturn:
        pytest.fail(f"{case.file}:{case.line}: {msg}", pytrace=False)

    # Process the parsed items. Each item has a header of form [id args],
    # optionally followed by lines of text.
    item = first_item = test_items[0]
    test_modules.append("__main__")
    for item in test_items[1:]:

        def _item_fail(msg: str) -> NoReturn:
            item_abs_line = case.line + item.line - 2
            pytest.fail(f"{case.file}:{item_abs_line}: {msg}", pytrace=False)

        if item.id in {"file", "fixture", "outfile", "outfile-re"}:
            # Record an extra file needed for the test case.
            assert item.arg is not None
            contents = expand_variables("\n".join(item.data))
            path = join(base_path, item.arg)
            if item.id != "fixture":
                test_modules.append(_file_arg_to_module(item.arg))
            if item.id in {"file", "fixture"}:
                files.append((path, contents))
            elif item.id == "outfile-re":
                output_files.append((path, re.compile(contents.rstrip(), re.S)))
            elif item.id == "outfile":
                output_files.append((path, contents))
        elif item.id == "builtins":
            # Use an alternative stub file for the builtins module.
            assert item.arg is not None
            mpath = join(os.path.dirname(case.file), item.arg)
            with open(mpath, encoding="utf8") as f:
                files.append((join(base_path, "builtins.pyi"), f.read()))
        elif item.id == "typing":
            # Use an alternative stub file for the typing module.
            assert item.arg is not None
            src_path = join(os.path.dirname(case.file), item.arg)
            with open(src_path, encoding="utf8") as f:
                files.append((join(base_path, "typing.pyi"), f.read()))
        elif item.id == "_typeshed":
            # Use an alternative stub file for the _typeshed module.
            assert item.arg is not None
            src_path = join(os.path.dirname(case.file), item.arg)
            with open(src_path, encoding="utf8") as f:
                files.append((join(base_path, "_typeshed.pyi"), f.read()))
        elif re.match(r"stale[0-9]*$", item.id):
            passnum = 1 if item.id == "stale" else int(item.id[len("stale") :])
            assert passnum > 0
            modules = set() if item.arg is None else {t.strip() for t in item.arg.split(",")}
            stale_modules[passnum] = modules
        elif re.match(r"rechecked[0-9]*$", item.id):
            passnum = 1 if item.id == "rechecked" else int(item.id[len("rechecked") :])
            assert passnum > 0
            modules = set() if item.arg is None else {t.strip() for t in item.arg.split(",")}
            rechecked_modules[passnum] = modules
        elif re.match(r"targets[0-9]*$", item.id):
            passnum = 1 if item.id == "targets" else int(item.id[len("targets") :])
            assert passnum > 0
            reprocessed = [] if item.arg is None else [t.strip() for t in item.arg.split(",")]
            targets[passnum] = reprocessed
        elif item.id == "delete":
            # File/directory to delete during a multi-step test case
            assert item.arg is not None
            m = re.match(r"(.*)\.([0-9]+)$", item.arg)
            if m is None:
                _item_fail(f"Invalid delete section {item.arg!r}")
            num = int(m.group(2))
            if num < 2:
                _item_fail(f"Can't delete during step {num}")
            full = join(base_path, m.group(1))
            deleted_paths.setdefault(num, set()).add(full)
        elif re.match(r"out[0-9]*$", item.id):
            if item.arg is None:
                args = []
            else:
                args = item.arg.split(",")

            version_check = True
            for arg in args:
                if arg.startswith("version"):
                    compare_op = arg[7:9]
                    if compare_op not in {">=", "=="}:
                        _item_fail("Only >= and == version checks are currently supported")
                    version_str = arg[9:]
                    try:
                        version = tuple(int(x) for x in version_str.split("."))
                    except ValueError:
                        _item_fail(f"{version_str!r} is not a valid python version")
                    if compare_op == ">=":
                        if version <= defaults.PYTHON3_VERSION:
                            _item_fail(
                                f"{arg} always true since minimum runtime version is {defaults.PYTHON3_VERSION}"
                            )
                        version_check = sys.version_info >= version
                    elif compare_op == "==":
                        if version < defaults.PYTHON3_VERSION:
                            _item_fail(
                                f"{arg} always false since minimum runtime version is {defaults.PYTHON3_VERSION}"
                            )
                        if not 1 < len(version) < 4:
                            _item_fail(
                                f'Only minor or patch version checks are currently supported with "==": {version_str!r}'
                            )
                        version_check = sys.version_info[: len(version)] == version
            if version_check:
                tmp_output = [expand_variables(line) for line in item.data]
                if os.path.sep == "\\" and case.normalize_output:
                    tmp_output = [fix_win_path(line) for line in tmp_output]
                if item.id == "out" or item.id == "out1":
                    output = tmp_output
                else:
                    passnum = int(item.id[len("out") :])
                    assert passnum > 1
                    output2[passnum] = tmp_output
                out_section_missing = False
        elif item.id == "triggered" and item.arg is None:
            triggered = item.data
        else:
            section_str = item.id + (f" {item.arg}" if item.arg else "")
            _item_fail(f"Invalid section header [{section_str}] in case {case.name!r}")

    if out_section_missing:
        _case_fail(f"Required output section not found in case {case.name!r}")

    for passnum in stale_modules.keys():
        if passnum not in rechecked_modules:
            # If the set of rechecked modules isn't specified, make it the same as the set
            # of modules with a stale public interface.
            rechecked_modules[passnum] = stale_modules[passnum]
        if (
            passnum in stale_modules
            and passnum in rechecked_modules
            and not stale_modules[passnum].issubset(rechecked_modules[passnum])
        ):
            _case_fail(f"Stale modules after pass {passnum} must be a subset of rechecked modules")

    output_inline_start = len(output)
    input = first_item.data
    expand_errors(input, output, "main")
    for file_path, contents in files:
        expand_errors(contents.split("\n"), output, file_path)

    seen_files = set()
    for file, _ in files:
        if file in seen_files:
            _case_fail(f"Duplicated filename {file}. Did you include it multiple times?")

        seen_files.add(file)

    case.input = input
    case.output = output
    case.output_inline_start = output_inline_start
    case.output2 = output2
    case.last_line = case.line + item.line + len(item.data) - 2
    case.files = files
    case.output_files = output_files
    case.expected_stale_modules = stale_modules
    case.expected_rechecked_modules = rechecked_modules
    case.deleted_paths = deleted_paths
    case.triggered = triggered or []
    case.expected_fine_grained_targets = targets
    case.test_modules = test_modules

