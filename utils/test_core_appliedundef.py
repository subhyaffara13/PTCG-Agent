
def test_core_appliedundef():
    x = Symbol("_long_unique_name_1")
    f = Function("_long_unique_name_2")
    check(f(x))

