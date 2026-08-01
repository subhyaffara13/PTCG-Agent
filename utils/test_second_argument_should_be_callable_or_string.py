
def test_second_argument_should_be_callable_or_string():
    raises(TypeError, lambda: raises("irrelevant", 42))

