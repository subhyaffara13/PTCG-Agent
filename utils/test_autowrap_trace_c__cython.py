
def test_autowrap_trace_C_Cython():
    has_module('Cython')
    runtest_autowrap_trace('C99', 'cython')

