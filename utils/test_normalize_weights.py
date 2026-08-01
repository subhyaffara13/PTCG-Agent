
def test_normalize_weights():
    assert _normalize_weight(300) == 300  # passthrough
    assert _normalize_weight('ultralight') == 100
    assert _normalize_weight('light') == 200
    assert _normalize_weight('normal') == 400
    assert _normalize_weight('regular') == 400
    assert _normalize_weight('book') == 400
    assert _normalize_weight('medium') == 500
    assert _normalize_weight('roman') == 500
    assert _normalize_weight('semibold') == 600
    assert _normalize_weight('demibold') == 600
    assert _normalize_weight('demi') == 600
    assert _normalize_weight('bold') == 700
    assert _normalize_weight('heavy') == 800
    assert _normalize_weight('extra bold') == 800
    assert _normalize_weight('black') == 900
    with pytest.raises(KeyError):
        _normalize_weight('invalid')

