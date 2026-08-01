
def test_multiple_same_figure_calls():
    fig = plt.figure(1, figsize=(1, 2))
    with pytest.warns(UserWarning, match="Ignoring specified arguments in this call"):
        fig2 = plt.figure(1, figsize=np.array([3, 4]))
    with pytest.warns(UserWarning, match="Ignoring specified arguments in this call"):
        plt.figure(fig, figsize=np.array([5, 6]))
    assert fig is fig2
    fig3 = plt.figure(1)  # Checks for false warnings
    assert fig is fig3

