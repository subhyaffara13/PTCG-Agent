
def test_python_keyword_symbol_name_escaping():
    # Check for escaping of keywords
    assert python(
        5*Symbol("lambda")) == "lambda_ = Symbol('lambda')\ne = 5*lambda_"
    assert (python(5*Symbol("lambda") + 7*Symbol("lambda_")) ==
            "lambda__ = Symbol('lambda')\nlambda_ = Symbol('lambda_')\ne = 7*lambda_ + 5*lambda__")
    assert (python(5*Symbol("for") + Function("for_")(8)) ==
            "for__ = Symbol('for')\nfor_ = Function('for_')\ne = 5*for__ + for_(8)")

