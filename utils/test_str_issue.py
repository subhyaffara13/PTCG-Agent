
def test_str_issue(msg):
    """#283: __str__ called on uninitialized instance when constructor arguments invalid"""

    assert str(m.StrIssue(3)) == "StrIssue[3]"

    with pytest.raises(TypeError) as excinfo:
        str(m.StrIssue("no", "such", "constructor"))
    assert (
        msg(excinfo.value)
        == """
        __init__(): incompatible constructor arguments. The following argument types are supported:
            1. m.methods_and_attributes.StrIssue(arg0: int)
            2. m.methods_and_attributes.StrIssue()

        Invoked with: 'no', 'such', 'constructor'
    """
    )

