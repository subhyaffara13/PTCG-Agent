
def test_figsize_invalid_unit():
    with pytest.raises(ValueError, match="Invalid unit 'um'"):
        plt.figure(figsize=(6, 4, "um"))

