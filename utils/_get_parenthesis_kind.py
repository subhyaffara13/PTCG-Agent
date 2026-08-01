
def _get_parenthesis_kind(s):
    assert s.startswith('@__f2py_PARENTHESIS_'), s
    return s.split('_')[4]

