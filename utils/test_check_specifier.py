
def test_check_specifier():
    # valid specifier value
    attrs = {'name': 'foo', 'python_requires': '>=3.0, !=3.1'}
    dist = Distribution(attrs)
    check_specifier(dist, attrs, attrs['python_requires'])

    attrs = {'name': 'foo', 'python_requires': ['>=3.0', '!=3.1']}
    dist = Distribution(attrs)
    check_specifier(dist, attrs, attrs['python_requires'])

    # invalid specifier value
    attrs = {'name': 'foo', 'python_requires': '>=invalid-version'}
    with pytest.raises(DistutilsSetupError):
        dist = Distribution(attrs)

