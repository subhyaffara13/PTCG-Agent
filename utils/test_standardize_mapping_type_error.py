
def test_standardize_mapping_type_error(into, msg):
    with pytest.raises(TypeError, match=msg):
        com.standardize_mapping(into)

