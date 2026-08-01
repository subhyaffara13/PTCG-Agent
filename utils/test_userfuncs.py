
def test_userfuncs():
    # Dictionary mutation test
    some_function = symbols("some_function", cls=Function)
    my_user_functions = {"some_function": "SomeFunction"}
    assert mcode(
        some_function(z),
        user_functions=my_user_functions) == \
        'SomeFunction[z]'
    assert mcode(
        some_function(z),
        user_functions=my_user_functions) == \
        'SomeFunction[z]'

    # List argument test
    my_user_functions = \
        {"some_function": [(lambda x: True, "SomeOtherFunction")]}
    assert mcode(
        some_function(z),
        user_functions=my_user_functions) == \
        'SomeOtherFunction[z]'

