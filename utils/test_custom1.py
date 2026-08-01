
def test_custom1():
    # Removes the parser's ability to understand \cdot and \div.

    parser = init_custom_parser(modification1)

    with raises(lark.exceptions.UnexpectedCharacters):
        parser.doparse(r"a \cdot b")
        parser.doparse(r"x \div y")

