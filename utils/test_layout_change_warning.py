
def test_layout_change_warning(layout):
    """
    Raise a warning when a previously assigned layout changes to tight using
    plt.tight_layout().
    """
    fig, ax = plt.subplots(layout=layout)
    with pytest.warns(UserWarning, match='The figure layout has changed to'):
        plt.tight_layout()

