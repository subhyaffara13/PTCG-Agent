
def get_completion_inspect_parameters() -> tuple[ParamMeta, ParamMeta]:
    completion_init()
    test_disable_detection = os.getenv("_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION")
    if not test_disable_detection:
        parameters = get_params_from_function(_install_completion_placeholder_function)
    else:
        parameters = get_params_from_function(
            _install_completion_no_auto_placeholder_function
        )
    install_param, show_param = parameters.values()
    return install_param, show_param

