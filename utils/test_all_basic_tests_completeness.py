
def test_all_basic_tests_completeness():
    num_found = 0
    for key, value in VARS_BEFORE_ALL_BASIC_TESTS.items():
        if not key.startswith("test_"):
            continue
        assert value in ALL_BASIC_TESTS
        num_found += 1
    assert len(ALL_BASIC_TESTS) == num_found

