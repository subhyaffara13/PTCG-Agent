
def get_semanal_options(program_text: str, testcase: DataDrivenTestCase) -> Options:
    options = parse_options(program_text, testcase, 1)
    options.use_builtins_fixtures = True
    options.semantic_analysis_only = True
    options.show_traceback = True
    options.python_version = PYTHON3_VERSION
    options.reveal_verbose_types = True
    return options

