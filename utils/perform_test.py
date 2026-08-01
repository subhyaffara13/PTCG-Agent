
def perform_test(
    func: Callable[[DataDrivenTestCase], None], builtins_path: str, testcase: DataDrivenTestCase
) -> None:
    for path, _ in testcase.files:
        if os.path.basename(path) == "builtins.py":
            default_builtins = False
            break
    else:
        # Use default builtins.
        builtins = os.path.join(test_temp_dir, "builtins.py")
        shutil.copyfile(builtins_path, builtins)
        default_builtins = True

    # Actually perform the test case.
    func(testcase)

    if default_builtins:
        # Clean up.
        os.remove(builtins)

