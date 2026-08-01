
def test_fancy():
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    ax.plot(np.arange(10), np.full(10, 5), np.full(10, 5), 'o--', label='line')
    ax.scatter(np.arange(10), np.arange(10, 0, -1), label='scatter')
    ax.errorbar(np.full(10, 5), np.arange(10), np.full(10, 10),
                xerr=0.5, zerr=0.5, label='errorbar')
    ax.legend(loc='lower left', ncols=2, title='My legend', numpoints=1)


def test_fancy():
    # using subplot triggers some offsetbox functionality untested elsewhere
    plt.subplot(121)
    plt.plot([5] * 10, 'o--', label='XX')
    plt.scatter(np.arange(10), np.arange(10, 0, -1), label='XX\nXX')
    plt.errorbar(np.arange(10), np.arange(10), xerr=0.5,
                 yerr=0.5, label='XX')
    plt.legend(loc="center left", bbox_to_anchor=[1.0, 0.5],
               ncols=2, shadow=True, title="My legend", numpoints=1)

