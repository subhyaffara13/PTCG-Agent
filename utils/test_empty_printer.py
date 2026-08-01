
def test_emptyPrinter():
    class MyObject:
        def __repr__(self):
            return "<MyObject with {...}>"

    # unknown objects are monospaced
    assert latex(MyObject()) == r"\mathtt{\text{<MyObject with \{...\}>}}"

    # even if they are nested within other objects
    assert latex((MyObject(),)) == r"\left( \mathtt{\text{<MyObject with \{...\}>}},\right)"


def test_empty_printer():
    str_printer = StrPrinter()
    assert str_printer.emptyPrinter("foo") == "foo"
    assert str_printer.emptyPrinter(x*y) == "x*y"
    assert str_printer.emptyPrinter(32) == "32"

