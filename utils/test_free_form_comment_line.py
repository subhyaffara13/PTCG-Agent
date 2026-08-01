
def test_free_form_comment_line():
    printer = FCodePrinter({'source_format': 'free'})
    lines = [ "! This is a long comment on a single line that must be wrapped properly to produce nice output"]
    expected = [
        '! This is a long comment on a single line that must be wrapped properly',
        '! to produce nice output']
    assert printer._wrap_fortran(lines) == expected

