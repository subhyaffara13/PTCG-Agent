
def _store_test_result(used_numexpr: bool) -> None:
    if used_numexpr:
        _TEST_RESULT.append(used_numexpr)

