
def test_warns_match_matching():
    with warnings.catch_warnings(record=True) as w:
        with warns(UserWarning, match='this is the warning message'):
            warnings.warn('this is the warning message', UserWarning)
        assert len(w) == 0

