
def test_C89CodePrinter():
    c89printer = C89CodePrinter()
    assert c89printer.language == 'C'
    assert c89printer.standard == 'C89'
    assert 'void' in c89printer.reserved_words
    assert 'template' not in c89printer.reserved_words
    assert c89printer.doprint(log10(x)) == 'log10(x)'

