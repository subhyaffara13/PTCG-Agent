
def find_test_dir() -> str | None:
    # Find the path to the dynamo expected failure and skip files.
    from os.path import abspath, basename, dirname, exists, join, normpath

    if sys.platform == "win32":
        return None

    # Check relative to this file (local build):
    test_dir = normpath(join(dirname(abspath(__file__)), "../../../test"))
    if exists(join(test_dir, "dynamo_expected_failures")):
        return test_dir

    # Check relative to __main__ (installed builds relative to test file):
    main = sys.modules["__main__"]
    file = getattr(main, "__file__", None)
    if file is None:
        # Generated files do not have a module.__file__
        return None
    test_dir = dirname(abspath(file))
    while dirname(test_dir) != test_dir:
        if basename(test_dir) == "test" and exists(
            join(test_dir, "dynamo_expected_failures")
        ):
            return test_dir
        test_dir = dirname(test_dir)

    # Not found
    return None

