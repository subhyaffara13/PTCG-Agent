
def LineMatcher_fixture(request: FixtureRequest) -> type[LineMatcher]:
    """A reference to the :class: `LineMatcher`.

    This is instantiable with a list of lines (without their trailing newlines).
    This is useful for testing large texts, such as the output of commands.
    """
    return LineMatcher

