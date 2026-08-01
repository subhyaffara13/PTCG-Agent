
def get_test_cases(*directories: str) -> list["ParameterSet"]:
    test_cases = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for fname in files:
                short_fname, ext = os.path.splitext(fname)
                if ext not in (".pyi", ".py"):
                    continue

                fullpath = os.path.join(root, fname)
                test_cases.append(pytest.param(fullpath, id=short_fname))
    return test_cases

