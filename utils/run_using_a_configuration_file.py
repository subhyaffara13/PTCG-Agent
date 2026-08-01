
def run_using_a_configuration_file(
    configuration_path: Path | str, file_to_lint: str = __file__
) -> Run:
    """Simulate a run with a configuration without really launching the checks."""
    configuration_path = str(configuration_path)
    args = ["--rcfile", configuration_path, file_to_lint]
    # Do not actually run checks, that could be slow. We don't mock
    # `PyLinter.check`: it calls `PyLinter.initialize` which is
    # needed to properly set up messages inclusion/exclusion
    # in `_msg_states`, used by `is_message_enabled`.
    check = "pylint.lint.pylinter.check_parallel"
    with unittest.mock.patch(check):
        runner = Run(args, exit=False)
    return runner

