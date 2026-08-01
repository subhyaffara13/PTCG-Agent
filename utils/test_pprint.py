
def test_pprint():
    import sys
    from io import StringIO
    fd = StringIO()
    sso = sys.stdout
    sys.stdout = fd
    try:
        pprint(pi, use_unicode=False, wrap_line=False)
    finally:
        sys.stdout = sso
    assert fd.getvalue() == 'pi\n'

