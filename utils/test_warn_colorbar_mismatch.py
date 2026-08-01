
def test_warn_colorbar_mismatch():
    fig1, ax1 = plt.subplots()
    fig2, (ax2_1, ax2_2) = plt.subplots(2)
    im = ax1.imshow([[1, 2], [3, 4]])

    fig1.colorbar(im)  # should not warn
    with pytest.warns(UserWarning, match="different Figure"):
        fig2.colorbar(im)
    # warn mismatch even when the host figure is not inferred
    with pytest.warns(UserWarning, match="different Figure"):
        fig2.colorbar(im, ax=ax1)
    with pytest.warns(UserWarning, match="different Figure"):
        fig2.colorbar(im, ax=ax2_1)
    with pytest.warns(UserWarning, match="different Figure"):
        fig2.colorbar(im, cax=ax2_2)

    # edge case: only compare top level artist in case of subfigure
    fig3 = plt.figure()
    fig4 = plt.figure()
    subfig3_1 = fig3.subfigures()
    subfig3_2 = fig3.subfigures()
    subfig4_1 = fig4.subfigures()
    ax3_1 = subfig3_1.subplots()
    ax3_2 = subfig3_1.subplots()
    ax4_1 = subfig4_1.subplots()
    im3_1 = ax3_1.imshow([[1, 2], [3, 4]])
    im3_2 = ax3_2.imshow([[1, 2], [3, 4]])
    im4_1 = ax4_1.imshow([[1, 2], [3, 4]])

    fig3.colorbar(im3_1)   # should not warn
    subfig3_1.colorbar(im3_1)   # should not warn
    subfig3_1.colorbar(im3_2)   # should not warn
    with pytest.warns(UserWarning, match="different Figure"):
        subfig3_1.colorbar(im4_1)

