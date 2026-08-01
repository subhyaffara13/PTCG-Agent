
def test_import_avoid_stl_array():
    pytest.importorskip("eigen_tensor_avoid_stl_array")
    assert len(submodules) == 4

