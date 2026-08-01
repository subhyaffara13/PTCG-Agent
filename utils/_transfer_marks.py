
def _transfer_marks(engine, read_ext):
    """
    engine gives us a pytest.param object with some marks, read_ext is just
    a string.  We need to generate a new pytest.param inheriting the marks.
    """
    values = (*engine.values, read_ext)
    new_param = pytest.param(values, marks=engine.marks)
    return new_param

