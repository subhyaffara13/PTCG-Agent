
def test_savefig_warns():
    fig = plt.figure()
    for format in ['png', 'pdf', 'svg', 'tif', 'jpg']:
        with pytest.raises(TypeError):
            fig.savefig(io.BytesIO(), format=format, non_existent_kwarg=True)

