
def test_imps_wrong_args():
    raises(ValueError, lambda: implemented_function(sin, lambda x: x))

