
def test_inherit_docstring_from():

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)

        class Foo:
            def func(self):
                '''Do something useful.'''
                return

            def func2(self):
                '''Something else.'''

        class Bar(Foo):
            @doccer.inherit_docstring_from(Foo)
            def func(self):
                '''%(super)sABC'''
                return

            @doccer.inherit_docstring_from(Foo)
            def func2(self):
                # No docstring.
                return

    assert_equal(Bar.func.__doc__, Foo.func.__doc__ + 'ABC')
    assert_equal(Bar.func2.__doc__, Foo.func2.__doc__)
    bar = Bar()
    assert_equal(bar.func.__doc__, Foo.func.__doc__ + 'ABC')
    assert_equal(bar.func2.__doc__, Foo.func2.__doc__)

