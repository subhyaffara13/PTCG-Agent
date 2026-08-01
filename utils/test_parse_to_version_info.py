
def test_parse_to_version_info(version_str, version_tuple):
    assert matplotlib._parse_to_version_info(version_str) == version_tuple

