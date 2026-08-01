
def test_validate_linespacing():
    with pytest.raises(TypeError):
        plt.text(.25, .5, "foo", linespacing="abc")

