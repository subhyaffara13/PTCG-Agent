
def test_colorbar_format_string_and_old():
    plt.imshow([[0, 1]])
    cb = plt.colorbar(format="{x}%")
    assert isinstance(cb._formatter, StrMethodFormatter)

