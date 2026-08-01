
def test_font_match_warning(caplog):
    findfont(FontProperties(family=["DejaVu Sans"], weight=750))
    logs = [rec.message for rec in caplog.records]
    assert 'findfont: Failed to find font weight 750, now using 700.' in logs

