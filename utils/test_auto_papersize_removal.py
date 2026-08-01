
def test_auto_papersize_removal():
    fig = plt.figure()
    with pytest.raises(ValueError, match="'auto' is not a valid value"):
        fig.savefig(io.BytesIO(), format='eps', papertype='auto')

    with pytest.raises(ValueError, match="'auto' is not a valid value"):
        mpl.rcParams['ps.papersize'] = 'auto'

