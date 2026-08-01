
def test_legend_title_fontprop_fontsize():
    # test the title_fontsize kwarg
    plt.plot(range(10), label="mock data")
    with pytest.raises(ValueError):
        plt.legend(title='Aardvark', title_fontsize=22,
                   title_fontproperties={'family': 'serif', 'size': 22})

    leg = plt.legend(title='Aardvark', title_fontproperties=FontProperties(
                                       family='serif', size=22))
    assert leg.get_title().get_size() == 22

    fig, axes = plt.subplots(2, 3, figsize=(10, 6))
    axes = axes.flat
    axes[0].plot(range(10), label="mock data")
    leg0 = axes[0].legend(title='Aardvark', title_fontsize=22)
    assert leg0.get_title().get_fontsize() == 22
    axes[1].plot(range(10), label="mock data")
    leg1 = axes[1].legend(title='Aardvark',
                          title_fontproperties={'family': 'serif', 'size': 22})
    assert leg1.get_title().get_fontsize() == 22
    axes[2].plot(range(10), label="mock data")
    mpl.rcParams['legend.title_fontsize'] = None
    leg2 = axes[2].legend(title='Aardvark',
                          title_fontproperties={'family': 'serif'})
    assert leg2.get_title().get_fontsize() == mpl.rcParams['font.size']
    axes[3].plot(range(10), label="mock data")
    leg3 = axes[3].legend(title='Aardvark')
    assert leg3.get_title().get_fontsize() == mpl.rcParams['font.size']
    axes[4].plot(range(10), label="mock data")
    mpl.rcParams['legend.title_fontsize'] = 20
    leg4 = axes[4].legend(title='Aardvark',
                          title_fontproperties={'family': 'serif'})
    assert leg4.get_title().get_fontsize() == 20
    axes[5].plot(range(10), label="mock data")
    leg5 = axes[5].legend(title='Aardvark')
    assert leg5.get_title().get_fontsize() == 20

