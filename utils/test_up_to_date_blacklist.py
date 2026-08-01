
def test_up_to_date_blacklist():
    assert mpl.style.core.STYLE_BLACKLIST <= {*mpl.rcsetup._validators}

