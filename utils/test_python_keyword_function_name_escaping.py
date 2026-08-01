
def test_python_keyword_function_name_escaping():
    assert python(
        5*Function("for")(8)) == "for_ = Function('for')\ne = 5*for_(8)"

