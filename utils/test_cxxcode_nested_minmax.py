
def test_cxxcode_nested_minmax():
    assert cxxcode(Max(Min(x, y), Min(u, v))) \
        == 'std::max(std::min(u, v), std::min(x, y))'
    assert cxxcode(Min(Max(x, y), Max(u, v))) \
        == 'std::min(std::max(u, v), std::max(x, y))'

