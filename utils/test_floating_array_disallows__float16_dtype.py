
def test_floating_array_disallows_Float16_dtype(request):
    # GH#44715
    with pytest.raises(TypeError, match="data type 'Float16' not understood"):
        pd.array([1.0, 2.0], dtype="Float16")

