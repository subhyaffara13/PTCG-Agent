
def test_title_location_roundtrip():
    fig, ax = plt.subplots()
    # set default title location
    plt.rcParams['axes.titlelocation'] = 'center'
    ax.set_title('aardvark')
    ax.set_title('left', loc='left')
    ax.set_title('right', loc='right')

    assert 'left' == ax.get_title(loc='left')
    assert 'right' == ax.get_title(loc='right')
    assert 'aardvark' == ax.get_title(loc='center')

    with pytest.raises(ValueError):
        ax.get_title(loc='foo')
    with pytest.raises(ValueError):
        ax.set_title('fail', loc='foo')

