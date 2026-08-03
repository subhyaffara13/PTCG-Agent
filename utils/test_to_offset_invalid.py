import re

def test_to_offset_invalid(freqstr):
    # see gh-13930

    # We escape string because some of our
    # inputs contain regex special characters.
    msg = re.escape(f"Invalid frequency: {freqstr}")
    with pytest.raises(ValueError, match=msg):
        to_offset(freqstr)

