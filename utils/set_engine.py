
def set_engine(engine, ext):
    """
    Fixture to set engine for use in each test case.

    Rather than requiring `engine=...` to be provided explicitly as an
    argument in each test, this fixture sets a global option to dictate
    which engine should be used to write Excel files. After executing
    the test it rolls back said change to the global option.
    """
    option_name = f"io.excel.{ext.strip('.')}.writer"
    with option_context(option_name, engine):
        yield

