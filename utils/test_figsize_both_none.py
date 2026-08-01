
def test_figsize_both_none():
    with pytest.raises(ValueError,
                       match=r"figsize=\(None, None\) is invalid"):
        plt.figure(figsize=(None, None))

