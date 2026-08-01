
def test_has_function_prototype():
    # Issue https://github.com/pypa/setuptools/issues/3648
    # Test prototype-generating behavior.

    compiler = base.new_compiler()

    # Every C implementation should have these.
    assert compiler.has_function('abort')
    assert compiler.has_function('exit')
    with pytest.deprecated_call(match='includes is deprecated'):
        # abort() is a valid expression with the <stdlib.h> prototype.
        assert compiler.has_function('abort', includes=['stdlib.h'])
    with pytest.deprecated_call(match='includes is deprecated'):
        # But exit() is not valid with the actual prototype in scope.
        assert not compiler.has_function('exit', includes=['stdlib.h'])
    # And setuptools_does_not_exist is not declared or defined at all.
    assert not compiler.has_function('setuptools_does_not_exist')
    with pytest.deprecated_call(match='includes is deprecated'):
        assert not compiler.has_function(
            'setuptools_does_not_exist', includes=['stdio.h']
        )

