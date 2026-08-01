
def test_color_override_warning(kwarg):
    with pytest.warns(UserWarning,
                      match="Setting the 'color' property will override "
                            "the edgecolor or facecolor properties."):
        Patch(color='black', **{kwarg: 'black'})

