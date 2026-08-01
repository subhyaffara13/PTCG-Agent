
def test_colorbar_errors(kwargs, error, message):
    fig, ax = plt.subplots()
    im = ax.imshow([[0, 1], [2, 3]])
    if kwargs.get('cax', None) is True:
        kwargs['cax'] = ax.inset_axes([0, 1.05, 1, 0.05])
    with pytest.raises(error, match=message):
        fig.colorbar(im, **kwargs)

