
def test_center_invalid():
    # GH 20647
    df = DataFrame()
    with pytest.raises(TypeError, match=".* got an unexpected keyword"):
        df.expanding(center=True)

