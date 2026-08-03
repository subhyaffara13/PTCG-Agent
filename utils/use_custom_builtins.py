import os

def use_custom_builtins(builtins_path: str, testcase: DataDrivenTestCase) -> Iterator[None]:
    for path, _ in testcase.files:
        if os.path.basename(path) == "builtins.pyi":
            default_builtins = False
            break
    else:
        # Use default builtins.
        builtins = os.path.abspath(os.path.join(test_temp_dir, "builtins.pyi"))
        shutil.copyfile(builtins_path, builtins)
        default_builtins = True

    # Actually perform the test case.
    try:
        yield None
    finally:
        if default_builtins:
            # Clean up.
            os.remove(builtins)

