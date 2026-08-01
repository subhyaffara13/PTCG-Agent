
def create_test_linter() -> PyLinter:
    test_reporter = GenericTestReporter()
    linter_ = PyLinter()
    linter_.set_reporter(test_reporter)
    linter_.config.persistent = 0
    checkers.initialize(linter_)
    return linter_

