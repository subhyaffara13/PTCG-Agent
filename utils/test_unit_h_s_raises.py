
def test_unit_H_S_raises(freq):
    # GH#59143
    msg = f"Invalid frequency: {freq}"

    with pytest.raises(ValueError, match=msg):
        Resolution.get_reso_from_freqstr(freq)

