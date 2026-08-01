
def test_deprecated_find_executable():
    with warns_deprecated_sympy():
        find_executable('python')

