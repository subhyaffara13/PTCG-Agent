
def test_live_issue_117():
    assert bin_to_gray('0100') == '0110'
    assert bin_to_gray('0101') == '0111'
    for bits in ('0100', '0101'):
        assert gray_to_bin(bin_to_gray(bits)) == bits

