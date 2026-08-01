
def check_skip(data, op_name):
    if isinstance(data.dtype, pd.BooleanDtype) and "sub" in op_name:
        pytest.skip("subtract not implemented for boolean")

