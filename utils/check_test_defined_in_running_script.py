
def check_test_defined_in_running_script(test_case):
    if running_script_path is None:
        return
    test_case_class_file = os.path.abspath(os.path.realpath(inspect.getfile(test_case.__class__)))
    if test_case_class_file != running_script_path:
        raise AssertionError(
            f'Class of loaded TestCase "{test_case.id()}" '
            f'is not defined in the running script "{running_script_path}", but in "{test_case_class_file}". Did you '
            "accidentally import a unittest.TestCase from another file?"
        )

